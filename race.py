import discord
from discord.ext import commands
from discord.ui import Button, View
import random


class MoveCarButton(Button):

  def __init__(self, player: int):
    super().__init__(style=discord.ButtonStyle.primary,
                     label=f"Roll Dice (Player {player + 1})")
    self.player = player

  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: RacingView = self.view

    if interaction.user.id != view.players[self.player]:
      await interaction.response.send_message("It's not your turn!",
                                              ephemeral=True)
      return

    dice_roll = random.randint(1, 6)
    view.positions[self.player] += dice_roll

    if view.positions[self.player] >= 10:
      content = f"🏁 Player {self.player + 1} wins with a roll of {dice_roll}! 🏁"
      for child in view.children:
        child.disabled = True
      view.stop()
    else:
      content = f"Player {self.player + 1} rolled a {dice_roll}.\n{view.render_track()}"

    await interaction.response.edit_message(content=content, view=view)


class RacingView(View):

  def __init__(self, cog, ctx, player1, player2):
    super().__init__()
    self.cog = cog
    self.ctx = ctx
    self.players = [player1.id, player2.id]
    self.positions = [0, 0]

    for i in range(2):
      self.add_item(MoveCarButton(i))

  def render_track(self):
    track = ['-' * 10 for _ in range(2)]
    for i, pos in enumerate(self.positions):
      track[i] = track[i][:pos] + '🚗' + track[i][pos + 1:]
    return "\n".join(track)


class RacingGame(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(guild_ids=[1066826355444027412],
                          name='race',
                          description='Start a racing game')
  async def start_race(self, ctx: discord.ApplicationContext,
                       opponent: discord.Member):
    view = RacingView(self, ctx, ctx.author, opponent)
    await ctx.respond(
        f"{ctx.author.display_name} challenges {opponent.display_name} to a race!\n{view.render_track()}",
        view=view)


def setup(bot):
  bot.add_cog(RacingGame(bot))
