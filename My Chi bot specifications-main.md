# My Chi bot specifications

---

# **Bot specification**

## **Features**:

1. ### Streak Counting on daily updates on study, certificates, personal project accomplishments, etc.

   1. Each update will give the users (*\~saiyans*) points (*\~Chi*).  
      1. 10 points for daily updates.  
      2. 5 points for same day updates.  
      3. (1/3) points will be deducted on daily streak misses, the deductions will be reflected on the next update by the user.  
         1. Ex:  if a user updates on 04-01-2025 and their last update was on 01-01-2025 i.e.,3 days of gap then the latest points given to the user will be 10 \- 1 \= 9\.  
         2. The point deduction will be reflected on the total points only when the gap is in multiples of 3\. The gaps of 1 and 2 will carry forward on the total gap counter.   
      4. Special points are provided:  
         1. Count streak \= 3 days then \+30 points instead of 10  
         2. Count streak \= 5 days then \+50 points instead of 10  
         3. Count streak \= 10 days then \+100 points instead of 10  
         4. Same day update \= 5 points instead of 10  
      5. Total points of each user categories them as corresponding modes/titles on the server.  
         1. Normal, if less than 100  
         2. Saiyan, if greater than 100 & less than 200  
         3. Super Saiyan, if greater than 200 & less than 300  
         4. Super Saiyan 2, if greater than 300 & less than 400  
         5. Super Saiyan 3, if greater than 400 & less than 500  
         6. Ultra-Instinct, if greater than 500

2. ### The Bot is configured to serve jokes and sarcasm.

3. ### The Bot also provides details of the top competitors and monthly top & bottom performers within the server.

## **Commands**:

1. ### **$coms**

   1. Use command to get all the available commands as well as their use case details within the bot’s ability.

2. ### **\>\>**

   1. Use \>\> in the first position of your update messages. Messages can contain plain texts as well as attached files. (\*imp: Use this to register yourself in the bot’s database before using other command features.)

3. ### **$mychi** 

   1. Use the command to get the details of your total points (Chi) , last update date, gaps, streak count/continuity.

4. ### **$my\_level**

   1. Use command to get the details of which mode/title you currently hold based on your total points.

5. ### **$fighters** 

   1. Use command to get the details of the top 5 competitors within the server.

6. ### **$mega\_star**

   1. Use command to get the details of the monthly top performer.

7. ### **$whos\_treat**

   1. Use command to get the details of the monthly bottom performer.

8. ### **$chi\_\<users\_discord\_username\>**

   1. Use command to get the particular user details.

9. ###  **$joke**

   1. Use command to get a joke in response.

10. ### **$burnMe**

    1. Use command to get sarcasm in response.

11. ###  **$levels**

    1. Use command to get the list of the mode categories.

12. ### **$\<any\_other\_message\>**

    1. will echo the message back along with a welcome and sarcastic response.

       

       

       

## Pitfalls:

1. The user data is stored in a simple csv file format and then imported as a pandas dataframe when queried by the users. This can be a bottleneck when the server hosts a large user base.

## Upcoming Features: 

1. A database storage instead of a csv format storage. (sql lite)  
2. Reminders of gaps with some texts.

