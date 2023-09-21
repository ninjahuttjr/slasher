import discord
from discord.ext import commands, tasks
from discord.ui import Select, View
from discord.components import SelectOption

import datetime
import pytz

class ReminderView(View):
    def __init__(self):
        super().__init__(timeout=60)  # View will stop listening after 60 seconds
        self.time_for_reminder = None  # Initialize the attribute

    @discord.ui.select(placeholder='Select the time for your reminder', min_values=1, max_values=1, options=[
        SelectOption(label='1 hour', value='1'),
        SelectOption(label='2 hours', value='2'),
        SelectOption(label='3 hours', value='3'),
        # Add more options as needed
    ])
    async def reminder_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        hours = int(select.values[0])
        self.time_for_reminder = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=hours)
        await interaction.response.send_message(f'Reminder set for {hours} hour(s) from now!', ephemeral=True)

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.slash_command(guild_ids=[1066826355444027412], name='reminder', description='Set a reminder')
    async def set_reminder(self, ctx: discord.ApplicationContext):
        view = ReminderView()
        await ctx.respond('When would you like to be reminded?', view=view)
        await view.wait()  # Wait for the view to finish
        if view.time_for_reminder:  # Check if the attribute is set
            self.reminders.append((ctx.author.id, view.time_for_reminder, ctx.channel.id))

    @tasks.loop(minutes=1)
    async def check_reminders(self):
        current_time = datetime.datetime.now(pytz.utc)
        for reminder in self.reminders:
            user_id, reminder_time, channel_id = reminder
            if current_time >= reminder_time:
                channel = self.bot.get_channel(channel_id)
                await channel.send(f"<@{user_id}> This is your reminder!")
                self.reminders.remove(reminder)

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.check_reminders.cancel()

def setup(bot):
    reminder_cog = Reminder(bot)
    bot.add_cog(reminder_cog)
    reminder_cog.check_reminders.start()
