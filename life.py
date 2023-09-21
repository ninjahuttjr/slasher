import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
from discord.ui import Button, View
import json
from datetime import datetime, timedelta

from functools import partial


# Functions to handle user data in a JSON file
def save_user_data(user_id, choice):
  with open('userdata.json', 'r') as f:
    data = json.load(f)
  data[str(user_id)] = {
      'choice': choice,
      'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  }
  with open('userdata.json', 'w') as f:
    json.dump(data, f)


def get_user_data(user_id):
  with open('userdata.json', 'r') as f:
    data = json.load(f)
  return data.get(str(user_id))


# Load game data from JSON
with open('life_choices.json', 'r') as f:
  game_data = json.load(f)

initial_choices = game_data['initial_choices']
subsequent_choices = game_data['subsequent_choices']


class DynamicLifeView(View):

  def __init__(self, cog, ctx, choices):
    super().__init__()
    self.cog = cog
    self.ctx = ctx
    for choice in choices:
      button = Button(label=choice['name'],
                      style=discord.ButtonStyle.primary,
                      custom_id=choice['name'])
      button.callback = partial(self.dynamic_button_callback, button)
      self.add_item(button)

  async def dynamic_button_callback(self, button: Button,
                                    interaction: discord.Interaction):
    choice_name = interaction.data['custom_id']
    await self.cog.send_time_passing_embed(interaction, choice_name)


class LifeGame(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def send_time_passing_embed(self, interaction, choice_name):
      # Update the user's choice first
      save_user_data(interaction.user.id, choice_name)

      # Now fetch the updated user data
      user_data = get_user_data(interaction.user.id)
      current_choice = user_data['choice'] if user_data else "None"

      description = next(
          (item['description']
          for item in initial_choices if item["name"] == choice_name), None)
      if not description:
          for key, values in subsequent_choices.items():
              description = next((item['description']
                                  for item in values if item["name"] == choice_name),
                                None)
              if description:
                  break

      embed = discord.Embed(title="Game of Life",
                            description=f"Your current choice is: **{current_choice}**\n\n{description}",
                            color=0xFFFFF)
      embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2017/06/19/07/13/live-2418343_1280.png")  # Add a relevant thumbnail
      embed.set_author(name=interaction.user.name,
                      icon_url=interaction.user.avatar.url)
      embed.set_footer(text="Disclaimer: This is a game, enjoy!")

      await interaction.response.edit_message(content="", embed=embed, view=None)



  @slash_command(guild_ids=[1066826355444027412],
                 name='life',
                 description='Start the Game of Life')
  async def start_life(self, ctx: discord.ApplicationContext):
    user_data = get_user_data(ctx.author.id)
    if user_data:
      last_choice = user_data['choice']
      choices = subsequent_choices.get(last_choice, [])
      if not choices:
        choices = initial_choices
      view = DynamicLifeView(self, ctx, choices)
      await ctx.respond(
          f"Based on your last choice: {last_choice}, what will you do next?",
          view=view)
    else:
      view = DynamicLifeView(self, ctx, initial_choices)
      await ctx.respond(
          "Welcome to the Game of Life! Let's start at the beginning. Who do you want to be?",
          view=view)

  @start_life.error
  async def start_life_error(self, ctx, error):
    if isinstance(error, CommandOnCooldown):
      await ctx.respond(
          "Check back in 10 minutes.. Years will have passed in the Game of Life, and new choices will await you!"
      )


def setup(bot):
  bot.add_cog(LifeGame(bot))
