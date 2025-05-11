#-------------Dependencies----------------#
import discord
from discord.ext import commands
import os
import csv
import datetime as dt
import pytz
import sqlite3
from dotenv import load_dotenv
import logging

#----------------- DATABASE-INITIALIZATION ------------------#

def init_database():
    """Initialize SQLite database and create necessary tables"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        # Create main chi_table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chi_table (
                id TEXT PRIMARY KEY,
                name TEXT,
                mychi INTEGER,
                gap INTEGER,
                continuity INTEGER,
                date TEXT,
                mode TEXT,
                reminder INTEGER
            )
        ''')
        # Create complements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complements (
                complement TEXT
            )
        ''')
        # Create jokes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jokes (
                joke TEXT
            )
        ''')
        conn.commit()


# Initialize database tables


# Import complements and jokes from CSV files (one-time operation)
def import_initial_data():
    """Import initial data from CSV files to SQLite tables"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        
           # Import complements using CSV reader
        with open('complements.csv', 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            cursor.executemany('INSERT INTO complements VALUES (?)', 
                                [(row[0],) for row in csv_reader])
        
        # Import jokes using CSV reader
        with open('jokes.csv', 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            cursor.executemany('INSERT INTO jokes VALUES (?)', 
                                [(row[0],) for row in csv_reader])
        
        conn.commit()




#-----------------Initialization-BLOCK-----------------------#

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=['$','>>'], intents=intents)

ist = pytz.timezone('Asia/Kolkata') # converting the UTC time to IST

today =  dt.datetime.now(ist) # today's date in datetime format

#--------------Logging function------------------#

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


#----------------------------------------------------------------------------#

#-------Database-Search-function------------------#
def saiyan_search(id):
    """Search for a saiyan by ID"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chi_table WHERE id = ?', (str(id),))
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'mychi': result[2],
                'gap': result[3],
                'continuity': result[4],
                'date': result[5],
                'mode' : result[6],
                'reminder' : result[7]
            }
    return None

def fighter_list():
    """Get top 5 fighters ordered by chi score"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM chi_table 
            ORDER BY mychi DESC, continuity DESC, date DESC, gap ASC 
            LIMIT 5
        ''')
        results = cursor.fetchall()
        return [{'id': r[0], 'name': r[1], 'mychi': r[2], 
                'gap': r[3], 'continuity': r[4], 'date': r[5], 'mode': r[6]} 
                for r in results]
    

#------------------------------------------------------#

#-----------------My-Saiyan-Mode----------------------------------------
def my_level(level):
    if level < 100:
        mode = 'Normal'
    elif level < 200:
        mode = 'Saiyan'
    elif level < 300: 
        mode = 'Super Saiyan'
    elif level < 400: 
        mode = 'Super Saiyan 2'
    elif level < 500: 
        mode = 'Super Saiyan 3'
    else:
        mode = 'Ultra Instinct'
    return mode

#-----------------Chi()-----------------#
def chi(id, name):
    """Update chi score for a user"""
    saiyan = saiyan_search(id)

    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        
        if not saiyan:
            # New user
            cursor.execute('''
                INSERT INTO chi_table (id, name, mychi, gap, continuity, date, mode, reminder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (str(id), 
                  str(name), 
                  10, 
                  0, 
                  0, 
                  today.strftime("%Y-%m-%d %H:%M:%S"),
                  "Normal",
                  0
                ))
            
            conn.commit()
            return 10
        
        # Existing user
        last_date = saiyan['date']
        last_dt = dt.datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ist)
        gap = (today - last_dt).days
        
        my_chi = saiyan['mychi']
        continuity = saiyan['continuity']
        new_gap = saiyan['gap']

        chi_points = 10
        chi_points_same_day = 5
        streak_3_points = 30
        streak_5_points = 50
        streak_10_points = 100


        # Calculate new chi based on gap
        if gap < 1:
            my_chi += chi_points_same_day
            continuity += 0
            new_gap = 0 
        elif gap == 1:
            new_gap = 0
            continuity += 1
            if continuity % 10 == 0:
                my_chi += streak_10_points
            elif continuity % 5 == 0:
                my_chi += streak_5_points
            elif continuity < 10 & continuity % 3 == 0:
                my_chi += streak_3_points
            else:
                my_chi += chi_points
        else:
            new_gap += gap
            continuity = 0
            if new_gap%3==0:
                penalty = round((new_gap / 3),0)
                my_chi += chi_points - penalty
                new_gap = 0
            else:
                penalty = round((new_gap / 3),0)
                my_chi += chi_points - penalty
                new_gap = gap % 3 
        mode = my_level(my_chi)

        # Update database
        cursor.execute('''
            UPDATE chi_table 
            SET mychi=?, gap=?, continuity=?, date=?, mode=?
            WHERE id=?
        ''', ( my_chi, new_gap, continuity, today.strftime("%Y-%m-%d %H:%M:%S"), mode,str(id)))
        conn.commit()
        return my_chi

#------------------Chi-Function-Calculator-End-------------------------#



#--------------------MOTIVATION_QUOTES----------------------------

def complements():
    """Get random complement"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT complement FROM complements ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()[0]

def jokes():
    """Get random joke"""
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT joke FROM jokes ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()[0]



#----------------------- Rank-Function -------------------------#
def Rank(id):
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        # Get lowest chi score
        cursor.execute('''
            WITH RankedUsers AS (
                SELECT 
                    id,
                    mychi,
                    RANK() OVER (
                        ORDER BY mychi DESC, 
                        continuity DESC, 
                        date DESC, 
                        gap ASC
                    ) as rank
                FROM chi_table
            )
            SELECT rank, mychi
            FROM RankedUsers
            WHERE id = ?
        ''',(str(id),))
        result = cursor.fetchone()
        if result is None:
            return None
        return result

#-------------------Role-assigning-----------------------------------------#

async def assign_role(ctx, user_id: int, role_name: str):
    guild = ctx.guild
    member = guild.get_member(user_id)
    if member is None:
        member = await guild.fetch_member(user_id)
        if not member:
            await ctx.send("User not found in the server.")
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
            await ctx.send("Role not found in the server.")
    if member and role:
        await member.add_roles(role)
        await ctx.send(f"Role '{role_name}' assigned to {member.display_name}.")


#-----------------End-of-Functions------------------------------#

#-----------------Bot_Events-Starts------------------------------------#

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    
    if message.author == bot.user:
        return
    else:
        if (message.content[:2]=='>>'):
            saiyan = saiyan_search(message.author.id)
            mode = saiyan['mode'] 
            await message.channel.send('We see a project update here, way to go man. Your Chi is being updated...')
            data = chi(message.author.id, message.author)
            await message.channel.send(f'Your Chi is now: {data}')
            new_role = my_level(data)
            if (mode != new_role):
                await assign_role(ctx, message.author.id,new_role)
        elif message.content == '$mychi':
            await bot.process_commands(message)

        elif message.content == '$joke':
            await bot.process_commands(message)
        
        elif message.content == "$burnMe":
            await bot.process_commands(message)
        
        elif message.content == "$fighters":
            data = fighter_list()
            for i in range(len(data)):
                await message.channel.send(f'**{data[i]['name']}**: {data[i]['mychi']} : {data[i]['mode']}')
            await bot.process_commands(message)
        
        elif message.content == "$my_mode":
            await bot.process_commands(message)
        
        elif message.content == "$coms":
            await bot.process_commands(message)
        
        elif message.content == "$whos_treat":
            await bot.process_commands(message)
        
        elif message.content == "$mega_star":
            await bot.process_commands(message)

        elif message.content[:5] == "$chi_":
            user = message.content[5:]
            with sqlite3.connect('chi_database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id,name,date,mode FROM chi_table 
                WHERE name = ?
            ''',(str(user),))
                result = cursor.fetchone()
            user_detail = result
            if not user_detail:
                sarcasm = complements()
                await message.channel.send('**404** User NOT FOUND')
                await message.channel.send('\n'+sarcasm)

            else:
                user_id = user_detail[0]
                name = user_detail[1]
                rank_result = Rank(user_id)
                if rank_result is None:
                    await message.channel.send(f"Could not retrieve ranking for {name}")
                    return
                rank, mychi = rank_result    
                mode = user_detail[3]
                last_update = user_detail[2]
                last_update_dt = dt.datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                formatted_date = last_update_dt.strftime("%d-%m-%Y")
                reply1 = f'**{name}** has Chi_score: **{mychi}**'
                reply2 = f'Saiyan Mode: **{mode}**\nOverall Rank in the server: **{rank}**'
                reply3 = f'Last learning/Project Update: **{formatted_date}**'
                await message.channel.send(reply1 + '\n' + reply2 + '\n' + reply3)
        elif message.content == '$modes':
            reply = f'*Normal*: **<100**\n*Saiyan*: **<200**\n*Super Saiyan*: **<300**\n*Super Saiyan 2*: **<400**\n*Super Saiyan 3*: **<500**\n*Ultra Instinct*: **>=500**'
            await message.channel.send(reply)
        else:
            if message.content[:1] == '$':
                author = message.author 
                reply1 = complements()
                reply2= f'Check **$coms** command to perform executable tasks.Cheers' 
                await message.channel.send(f'Yooo...\n**{author}**\n\n*{reply1}*\n\n{reply2}')

#-----------------End-of-BOT_EVENTS--------------------------------------#

#-----------------BOT_COMMANDS-BLOCKS------------------------------------#

#-------------------Coms-------------------------------------------------#
@bot.command()
async def coms(ctx):
    update = '**>>** : for any updates and gaining chi_scores'
    mychi = "**$mychi** : To check your Chi level"
    joke = "**$joke** : To get a joke"
    burnMe = "**$burnMe** : To get a saracastic compliment"
    fighters = "**$fighters** : To get the top 5 fighters"
    my_mode = "**$my_mode** : To check your mode"
    whos_treat = "**$whos_treat** : To know who's treating today"
    mega_star = "**$mega_star** : To know the MegaStar"
    user_detail = "**$chi_<discordUsername>**: to get deatails of the particular user. Ex: $chi_kni8goku"
    saiyan = f'**$modes** : to know the saiyan modes corresponding to the chi_scores.'
    await ctx.send(update+'\n'+mychi+'\n'+my_mode+'\n'+user_detail+'\n'+joke+'\n'+burnMe+'\n'+fighters+'\n'+whos_treat+'\n'+mega_star+'\n'+saiyan)

#-------------------mychi----------------------#
@bot.command()
async def mychi(ctx):
    # today = dt.datetime.now(ist)
    id = ctx.author.id
    name = ctx.author
    
    saiyan = saiyan_search(id)
    
    if not saiyan:
        chi_score = chi(id, name)
        await ctx.send(f'Looks like you are a new hustler, welcome **{name}** to the world of Saiyans.\nYou get a joining Chi_score: **{chi_score}**')
    else:
        chi_score = saiyan['mychi']
        continuity = saiyan['continuity']
        gap = saiyan['gap']
        mode = saiyan['mode']
        last_update = saiyan['date']
        last_update_dt = dt.datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
        formatted_date = last_update_dt.strftime("%d-%m-%Y")
        await ctx.send(f'As of {today.strftime("%d-%m-%Y")} \n\nYour Chi is: **{chi_score}** \nYour continuity is: **{continuity}** \nYour gap is: **{gap}** \nYou are in **{mode}** mode \n\nYour last update was on {formatted_date}')
    
#-------------------joke----------------------#
@bot.command()
async def joke(ctx):
    reply= jokes()
    await ctx.send(reply)

#-------------------burnMe----------------------#
@bot.command()
async def burnMe(ctx):
    reply= complements()
    await ctx.send(reply)

#-------------------fighters----------------------#
@bot.command()
async def fighters(ctx):
    result = Rank(ctx.author.id)
    if not result:
        await ctx.send(f'Looks like you are new here, register yourself by using **$mychi** command')
    rank, my_chi = result
    await ctx.send(f'Yoo {ctx.author} ,\n Your Rank is: **{rank}** and Chi_score: **{my_chi}**')

#-------------------my_mode bot call----------------------#
@bot.command()
async def my_mode(ctx):
    saiyan = saiyan_search(ctx.author.id)
    reply= saiyan['mode']
    if not reply:
        await ctx.send(f'Looks like you are new here, register yourself by using **$mychi** command')
    await ctx.send(f'Your mode is : **{reply}**')

#-------------------whos_treat()----------------------#
@bot.command()
async def whos_treat(ctx):
    # today = dt.datetime.now(ist)
    start_date = (today - dt.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        # Get lowest chi score
        cursor.execute('''
            SELECT name FROM chi_table 
            WHERE strftime('%s', date) >= strftime('%s', ?)
            ORDER BY mychi ASC, continuity ASC, date ASC, gap DESC 
            LIMIT 1
        ''', (start_date,))
        treat_giver = cursor.fetchone()
        treat_giver = treat_giver[0]
        if not treat_giver:
                await ctx.send("No activity found!")
                return
        # Get highest chi score
        cursor.execute('''
            SELECT name FROM chi_table 
            WHERE strftime('%s', date) >= strftime('%s', ?)
            ORDER BY mychi DESC, continuity DESC, date DESC, gap ASC 
            LIMIT 1
        ''', (start_date,))
        star = cursor.fetchone()
        star = star[0]
        if not star:
                await ctx.send("No activity found!")
                return
    reply1 = f'Is month ki party \n**{treat_giver}** ke taraf se.'
    reply2 = f'Is month ka Star, drumrolls please......\n **{star}**'
    await ctx.send('\n'+reply1 + '\n' + reply2)

#-------------------mega_star----------------------#
@bot.command()
async def mega_star(ctx):
    # df = df_update()
    # data = df.head().sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
    with sqlite3.connect('chi_database.db') as conn:
        cursor = conn.cursor()
        # Get lowest chi score
        cursor.execute('''
            SELECT  
            RANK() OVER(ORDER BY mychi DESC, continuity DESC, date DESC, gap ASC),
            mychi,
            mode
            FROM chi_table
            WHERE id = ?
            LIMIT 1 
        ''',(str(ctx.author.id),))
        result = cursor.fetchone()
        rank = result[0]
        my_chi = result[1]
        mode = result[2]
    await ctx.send(f'The MegaStar is: \n**{rank}. {ctx.author}** with a Chi of *{my_chi}* \nat Saiyan Mode: **{mode}**')

#-----------------End-of-BOT_COMMANDS-BLOCKS------------------------------#

#Load environment variables from .env file
load_dotenv()
#create a database
init_database()
#load data into database
import_initial_data()

#Get the token from the environment variables
token = os.getenv('TOKEN')

if token is None:
    raise ValueError("No TOKEN found in environment variables")

#Run the bot
bot.run(token)

#-----------------End-of-File------------------------------------#
