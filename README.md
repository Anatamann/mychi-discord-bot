# MyChi Bot 💥  
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3%2B-blue.svg)
![Discord Bot](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)

A Discord bot designed to track users' learning or project updates, reward consistency through a gamified points system, and add some fun through jokes and sarcasm.

---

> ⚠️ **Note:** This is a private bot. To use it, you must create your own Discord App via the [Discord Developer Portal](https://discord.com/developers) and host the bot independently on your machine or a 24/7 cloud provider.

We recommend [Sparked Host](https://billing.sparkedhost.com/aff.php?aff=2780) for 24/7 bot uptime.

---

## 🚀 Use Cases

1. Track your learning, certifications, or personal project updates.
2. Interact casually using built-in commands for jokes or sarcastic responses.
3. Compete with fellow users in your server via the point system and leaderboard.
4. Commands like `$whos_treat` and `$mega_star` keep the competition fun and engaging.

---

## ⚙️ Setup

### Requirements

- A Discord Bot Token ([Get it here](https://discord.com/developers))
- Python 3+
- Required dependencies listed in `requirements.txt`
  > 💡 Tip: Use Docker for deployment to avoid dependency conflicts. Be sure to configure `docker volumes` for **persistent user data**.

---

## 🧠 Specifications

### 🔁 Streak and Points Logic

Each update contributes to a user’s (*Saiyan's*) total **Chi** (points):

| Type                            | Chi Awarded |
|---------------------------------|-------------|
| Daily Update                    | +10         |
| Same-Day Additional Update      | +5          |
| Streak Miss Penalty (per 3-day) | −1          |

**Example**  
Update on 01-01-2025 → Next update on 04-01-2025 (3-day gap) → Chi = **9** (10 − 1)

#### ✅ Bonus Points for Streaks:
| Streak Length | Bonus Chi |
|---------------|-----------|
| 3 days        | +30       |
| 5 days        | +50       |
| 10 days       | +100      |

> Note: Point deduction affects total Chi only if the gap is a multiple of 3. Gaps of 1–2 days are carried forward cumulatively.

### 🧬 Titles / Power Levels

Your **Chi level** determines your title:

| Title             | Chi Range         |
|-------------------|-------------------|
| Normal            | < 100             |
| Saiyan            | 100 – 199         |
| Super Saiyan      | 200 – 299         |
| Super Saiyan 2    | 300 – 399         |
| Super Saiyan 3    | 400 – 499         |
| Ultra-Instinct    | 500+              |

---

- - - - 
## Commands ##

    $coms
   Use command to get all the available commands as well as their use case details within the bot’s ability.

    >>
   Use in the first position of your update messages. Messages can contain plain texts as well as attached files. (*imp: Use this to register yourself in the bot’s database before using other command features.)

    $mychi 
   Use the command to get the details of your total points (Chi) , last update date, gaps, streak count/continuity.
    
    $my_mode
   Use command to get the details of which mode/title you currently hold based on your total points.
    
    $fighters
   Use command to get the details of the top 5 competitors.

    $mega_star
   Use command to get the details of the monthly top performer.
    
    $whos_treat
   Use command to get the details of the monthly bottom performer.
    
    $chi_<users_discord_username>
   Use command to get the particular user details. (*Note:* Use the username and not the displayname of the user.)
    
    $joke
   Use command to get a joke in response.
   
    $burnMe
   Use command to get sarcasm in response.
   
    $modes
   Use command to get the list of the mode categories.
    
    $<any_other_message>
   Will echo the message back along with a welcome and sarcastic response.


---

## 🛠️ Upcoming Features

- 📦 ~~**Database Integration:** Move from flat-file (CSV) storage to **SQLite** for more efficient, scalable data handling.~~ ✅(05-05-2025)
- 🔔 **Automated Reminders:** Notify users about missed streaks and pending updates with fun & sarcastic nudges.
- 📈 **Progress Reports:** Weekly and monthly Chi gain summaries via DM or public leaderboard.
- 🌐 **Web Dashboard (optional):** Minimal web dashboard to view Chi history and update logs.
- 🧙‍♂️ **Role Syncing:** Automatically assign Discord roles based on Chi levels.
- ⏰ **Time-Zone Aware Logging:** Accurate update tracking across different user time zones.

---
## 🪪 License

This is a personal/hobby project maintained with ❤️ for fun and motivation.  
You're free to use, modify, or fork this bot for personal or server use.

**Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).**
