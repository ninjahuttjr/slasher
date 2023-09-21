# history.py

import discord
from discord.ext import commands, tasks
import datetime
import requests
import random

API_KEY = 'x0kPmYQDlM11v8ha5ir4LA==FSEGflmy7YYUS6NO'  # Replace with your API key
HEADERS = {
    'X-Api-Key': API_KEY
}


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_daily_fact.start()  # Start the background task

    def cog_unload(self):
        self.send_daily_fact.cancel()  # Stop the background task when the cog is unloaded

    @tasks.loop(minutes=1)  # Check every minute
    async def send_daily_fact(self):
        now = datetime.datetime.now()
        (f"Checking time: {now.hour}:{now.minute}")  # Logging current time
        if now.hour == 11 and now.minute == 49:
            print("Time matched!")  # Logging if time condition is met
            guild_id = 1066826355444027412  # Replace with your guild ID
            guild = self.bot.get_guild(guild_id)
    
            if not guild:
                print(f"Error: Couldn't find guild with ID {guild_id}")
                return
    
            channel = guild.system_channel  # Get the default system channel
    
            if not channel:
                print(f"Error: No system channel found for guild {guild.name}")
                return
    
            month, day = now.month, now.day
            url = f"https://api.api-ninjas.com/v1/historicalevents?month={month}&day={day}"
            response = requests.get(url, headers=HEADERS)
            
            # Print the API response for debugging
            print(f"API Response: {response.status_code}")
            print(f"API Data: {response.text}")
    
            if response.status_code != 200:
                print(f"API Error: {response.status_code}, {response.text}")  # Logging API errors
                return
    
            data = response.json()
            if not data:
                print("No historical events found for today.")
                return
        
            event = random.choice(data)  # Randomly select an event from the list
        
            await channel.send(f"On this day in history ({event['year']}): {event['event']}")
            print("Message sent!")  # Logging successful message send
        
              
    @send_daily_fact.before_loop
    async def before_send_daily_fact(self):
        await self.bot.wait_until_ready()
        print("Bot is ready!")  # Logging when bot is ready

def setup(bot):
    bot.add_cog(History(bot))
