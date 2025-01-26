#-------------Dependencies----------------#
import discord
from discord.ext import commands
import os
import random as rnd
# import csv
import pandas as pd
import datetime as dt
import pytz
from dotenv import load_dotenv

#-----------------END-Dependencies----------------------#

#-----------------Initialization-BLOCK-----------------------#

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=['$','>>'], intents=intents)

ist = pytz.timezone('Asia/Kolkata') #converting the UTC time to IST

data_file='chi_data.csv' #importing the csv datafile

#-------Dataframe-Update-function------------------#

def df_update():
    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'])
    return df
#------------------------------------------------------#

#-----------------Dataframe-Query-Block----------------------#
def saiyan_search(id):
    df = df_update()
    id_str = str(id)
    saiyan = df.query('id == @id_str')
    return saiyan

def fighter_list():
    df = df_update()
    data = df.head().sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
    #con_data = pd.concat([data,pd.DataFrame(saiyan)], ignore_index=True)
    return data

#------------------------------------------------------#


#-----Sarcastic-Compliments-file-------------------#

file_complements = "complements.csv"
complement_df = pd.read_csv(file_complements)

#------------Jokes-file-------------------#

file_jokes = "jokes.csv" 
jokes_df = pd.read_csv(file_jokes)

#------------------------------------------------------

#-----------------End-Initialization-BLOCK-------------------#

#-----------------Function-chi-level-Calculator-&-Update-----------------#
def chi(id, name):
    
    id_new = id
    today = dt.datetime.now(ist)
    saiyan = saiyan_search(id_new)

    if saiyan.empty:
        df = df_update()
        new_entry = {'id':id_new,'name': name,'mychi': 10.0, 'gap':0 , 'continuity': 0, 'date': today.strftime("%Y-%m-%d")}
        
        df_new = pd.concat([df,pd.DataFrame([new_entry])], ignore_index=True)
        df_new['date'] = pd.to_datetime(df_new['date'])
      
        df_new.to_csv(data_file, index=False) #update the csv file
        return df_new.mychi.values[len(df_new)-1]
    else:
        last_date = saiyan.date.dt.tz_localize(ist)
        gap = (today - last_date).dt.days.values[0]
        if gap == 0:
            continuity = saiyan.continuity.values[0]
            My_chi = saiyan.mychi.values[0] + 5.0
        elif gap == 1:
            gap = 0
            continuity = saiyan.continuity.values[0] + 1
            if continuity % 3 == 0:
                My_chi = saiyan.mychi.values[0] + 30.0
            elif continuity % 5 == 0:
                My_chi = saiyan.mychi.values[0] + 50.0
            elif continuity % 10 == 0:
                My_chi = saiyan.mychi.values[0] + 100.0
            else:
                My_chi = saiyan.mychi.values[0] + 10.0
        else:
            if gap%3==0:
                My_chi = saiyan.mychi.values[0] + 10.0 - gap
                gap = 0
                continuity = 0
            else:
                My_chi = round(saiyan.mychi.values[0],2) + 10.0 - round((gap/3),2) 
                gap = saiyan.gap.values[0] + gap%3
                continuity = 0
                
        updated_data = {
            'id':id, 
            'name':name, 
            'mychi': My_chi, 
            'gap':int(gap), 
            'continuity':int(continuity), 
            'date':today.strftime("%Y-%m-%d")
        }
        
        df = df_update()
        id_str = str(id)

        #Update the dataframe for the user

        df.loc[df['id'] == id_str, ['name', 'mychi', 'gap', 'continuity', 'date']] = [
        updated_data['name'],
        updated_data['mychi'],
        updated_data['gap'],
        updated_data['continuity'],
        updated_data['date']
        ] 

        df['date'] = pd.to_datetime(df['date'])

        df.to_csv(data_file, index=False) #update the csv file
        return My_chi

#------------------Chi-Function-Calculator-End-------------------------#



#--------------------MOTIVATION_QUOTES----------------------------

def complements():
    random = rnd.randint(0, 49)
    return (complement_df.iloc[random][0])

#--------------------Jokes_Quote---------------------------------

def jokes():
    random = rnd.randint(0, 49)
    return (jokes_df.iloc[random][0])

#-----------------My-Saiyan-Mode----------------------------------------
def my_mode(level):
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

#-----------------End-of-Functions------------------------------#

#-----------------BOT_EVENTS------------------------------------#

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    else:
        if (message.content[:2]=='>>'):
            await message.channel.send('We see a project update here, way to go man. Your Chi is being updated...')
            data = chi(message.author.id, message.author)
            await message.channel.send(f'Your Chi is now: {data}')
        
        elif message.content == '$mychi':
            await bot.process_commands(message)

        elif message.content == '$joke':
            await bot.process_commands(message)
        
        elif message.content == "$burnMe":
            await bot.process_commands(message)
        
        elif message.content == "$fighters":
            data = fighter_list()
            for i in range(len(data)):
                await message.channel.send(f'**{data.name.values[i]}**: {data.mychi.values[i]}')
            await bot.process_commands(message)
        
        elif message.content == "$my_level":
            await bot.process_commands(message)
        
        elif message.content == "$coms":
            await bot.process_commands(message)
        
        elif message.content == "$whos_treat":
            await bot.process_commands(message)
        
        elif message.content == "$mega_star":
            await bot.process_commands(message)

        elif message.content[:5] == "$chi_":
            user = message.content[5:]
            df = df_update()
            user_detail = df[df['name'].str.contains(f'^{user}$', regex=True)]
            if user_detail.empty:
                sarcasm = complements()
                await message.channel.send('**404** User NOT FOUND')
                await message.channel.send('\n'+sarcasm)

            else:
                name = user_detail.name.values[0]
                df_desc = df.sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
                rank = (df_desc.query('name == @name').index.values[0]) + 1 
                mode = my_mode(user_detail.mychi.values[0])
                last_update = user_detail.date.dt.strftime("%Y %m %d").values[0]
                reply1 = f'**{name}** has Chi_score: **{user_detail.mychi.values[0]}**'
                reply2 = f'Saiyan Mode: **{mode}**\nOverall Rank in the server:**{rank}**'
                reply3 = f'Last learning/Project Update: **{last_update}**'
                await message.channel.send(reply1 + '\n' + reply2 + '\n' + reply3)
        elif message.content == '$levels':
            reply = f'*Normal*: **<100**\n*Saiyan*: **<200**\n*Super Saiyan*: **<300**\n*Super Saiyan 2*: **<400**\n*Super Saiyan 3*: **<500**\n*Ultra Instinct*: **>=500**'
            await message.channel.send(reply)
        else:
            if message.content[:1] == '$':
                author = message.author 
                reply1 = complements()
                reply2= f'Check **$coms** command to perform executable tasks.Cheers' 
                await message.channel.send(f'Yooo...\n**{author}**\n\n*{reply1}*\n\n{reply2}')

#-----------------End-of-BOT_EVENTS------------------------------#

#-----------------BOT_COMMANDS-BLOCKS------------------------------------#

#-------------------coms----------------------#
@bot.command()
async def coms(ctx):
    update = '**>>** : for any updates and gaining chi_scores'
    mychi = "**$mychi** : To check your Chi level"
    joke = "**$joke** : To get a joke"
    burnMe = "**$burnMe** : To get a saracastic compliment"
    fighters = "**$fighters** : To get the top 5 fighters"
    my_level = "**$my_level** : To check your mode"
    whos_treat = "**$whos_treat** : To know who's treating today"
    mega_star = "**$mega_star** : To know the MegaStar"
    user_detail = "**$chi_<discordUsername>**: to get deatails of the particular user. Ex: $chi_kni8goku"
    saiyan = f'**$levels** : to know the saiyan modes corresponding to the chi_scores.'
    await ctx.send(update+'\n'+mychi+'\n'+my_level+'\n'+user_detail+'\n'+joke+'\n'+burnMe+'\n'+fighters+'\n'+whos_treat+'\n'+mega_star+'\n'+saiyan)

#-------------------mychi----------------------#
@bot.command()
async def mychi(ctx):
    today = dt.datetime.now(ist)
    id = ctx.author.id
    name = ctx.author
    
    saiyan = saiyan_search(id)
    
    if saiyan.empty:
        chi_score = chi(id, name)
        await ctx.send(f'Looks like you are a new hustler, welcome **{name}** to the world of Saiyans.\nYou get a joining Chi_score: **{chi_score}**')
    else:
        chi_score = saiyan.mychi.values[0]
        continuity = saiyan.continuity.values[0]
        gap = saiyan.gap.values[0]
        mode = my_mode(chi_score)
        date = saiyan.date.dt.date.values[0]
        await ctx.send(f'As of {today.strftime("%Y-%m-%d")} \n\nYour Chi is: **{chi_score}** \nYour continuity is: **{continuity}** \nYour gap is: **{gap}** \nYou are in **{mode}** mode \n\nYour last update was on {date}')
    
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
    df = df_update()
    saiyan = saiyan_search(ctx.author.id)
    data = df.sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
    rank = data.loc[data['id'] == str(ctx.author.id)].index[0]
    rank = rank + 1
    await ctx.send(f'Yoo {ctx.author} ,\n Your Rank is: **{rank}** and Chi_score: **{saiyan.mychi.values[0]}**')

#-------------------my_level----------------------#
@bot.command()
async def my_level(ctx):
    saiyan = saiyan_search(ctx.author.id)
    reply= my_mode(saiyan.mychi.values[0])
    await ctx.send(f'Your mode is : **{reply}**')

#-------------------whos_treat----------------------#
@bot.command()
async def whos_treat(ctx):
    df = df_update()
    today = dt.datetime.now(ist)
    start_date = today - dt.timedelta(days=30)
    start_date = start_date.strftime('%Y-%m-%d')
    data_asc = df.query('date >= @start_date').sort_values(by=['mychi','continuity','date','gap'], ascending=[True,True,True,False]).reset_index(drop=True)
    data_desc = df.query('date >= @start_date').sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
    reply1 = f'Is month ki party \n**{data_asc.name.values[0]}** ke taraf se.'
    reply2 = f'Is month ka Star, drumrolls please......\n **{data_desc.name.values[0]}**' 
    await ctx.send('\n'+reply1 + '\n' + reply2)

#-------------------mega_star----------------------#
@bot.command()
async def mega_star(ctx):
    df = df_update()
    data = df.head().sort_values(by=['mychi','continuity','date','gap'], ascending=[False,False,False,True]).reset_index(drop=True)
    mode = my_mode(data.mychi.values[0])
    await ctx.send(f'The MegaStar is: \n**{data.name.values[0]}** with a Chi of *{data.mychi.values[0]}* \nat Saiyan Mode: **{mode}**')

#-----------------End-of-BOT_COMMANDS-BLOCKS------------------------------#

#Load environment variables from .env file
load_dotenv()

#Get the token from the environment variables
token = os.getenv('TOKEN')

if token is None:
    raise ValueError("No TOKEN found in environment variables")

#Run the bot
bot.run(token)

#-----------------End-of-File------------------------------------#
