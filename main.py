import discord
import os

print(os.getcwd())

# import asyncio

bot = discord.Bot(intents=discord.Intents.all(), )


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')
  while True:
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Grizzly Man'))

  #     await asyncio.sleep(60)


extensions = [
    'cogs.ping',
    'cogs.life',
    'cogs.tic_tac_toe',  # Add this line
    'cogs.hangman',  # Add this line
    'cogs.chat',  # Add this line
    'cogs.race',  # Add this line
    'cogs.history',  # Add this line
    'cogs.hobbies',  # Add this line
    'cogs.reminders',  # Add this line
    'cogs.moderation',  # Add this line
    'cogs.scrape',  # Add this line
    'cogs.linux',  # Add this line
]

if __name__ == '__main__':
  for extension in extensions:
    bot.load_extension(extension)

bot.run(
    'MTA2MDM1NjgzNjMxMTcxNTg3MA.Ghh3Ot.oyZSsu52hiOoPAHLck49W5hm6PR4u-eDjFlf9Y'
)  # bot token
