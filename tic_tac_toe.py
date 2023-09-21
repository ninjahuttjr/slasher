import discord
from discord.ext import commands
from discord.ui import Button, View
from functools import partial


class TicTacToeButton(Button):

  def __init__(self, x: int, y: int):
    super().__init__(style=discord.ButtonStyle.secondary,
                     label="\u200b",
                     row=y)
    self.x = x
    self.y = y

  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: TicTacToeView = self.view

    # Check if the current player is the one who clicked the button
    if interaction.user.id != view.players[view.current_player]:
      await interaction.response.send_message("It's not your turn!",
                                              ephemeral=True)
      return

    if view.current_player == view.X:
      self.style = discord.ButtonStyle.danger
      self.label = "X"
      view.board[self.y][self.x] = view.X
      view.current_player = view.O
      content = "It is now O's turn"
    else:
      self.style = discord.ButtonStyle.success
      self.label = "O"
      view.board[self.y][self.x] = view.O
      view.current_player = view.X
      content = "It is now X's turn"

    self.disabled = True
    winner = view.check_winner()
    if winner is not None:
      if winner == view.X:
        content = "X won!"
      elif winner == view.O:
        content = "O won!"
      else:
        content = "It's a tie!"

      for child in view.children:
        child.disabled = True

      view.stop()

    await interaction.response.edit_message(content=content, view=view)


class TicTacToeView(View):
  X = -1
  O = 1
  Tie = 2

  def __init__(self, cog, ctx, player1, player2):
    super().__init__()
    self.cog = cog
    self.ctx = ctx
    self.players = {self.X: player1.id, self.O: player2.id}  # Store player IDs
    self.current_player = self.X
    self.board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    for x in range(3):
      for y in range(3):
        self.add_item(TicTacToeButton(x, y))

  def check_winner(self):
    # Check horizontal
    for row in self.board:
      value = sum(row)
      if value == 3:
        return self.O
      elif value == -3:
        return self.X

    # Check vertical
    for col in range(3):
      value = self.board[0][col] + self.board[1][col] + self.board[2][col]
      if value == 3:
        return self.O
      elif value == -3:
        return self.X

    # Check diagonals
    diag1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
    diag2 = self.board[0][2] + self.board[1][1] + self.board[2][0]
    if diag1 == 3 or diag2 == 3:
      return self.O
    elif diag1 == -3 or diag2 == -3:
      return self.X

    # Check for a tie
    if all(cell != 0 for row in self.board for cell in row):
      return self.Tie

    return None


class TicTacToe(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(
      guild_ids=[1066826355444027412, 759187011407052820, 1152046341615263744],
      name='ttt',
      description='Play Tic-Tac-Toe')
  async def start_ttt(self, ctx: discord.ApplicationContext,
                      opponent: discord.Member):
    view = TicTacToeView(self, ctx, ctx.author, opponent)

    # Respond with the game message
    game_message = await ctx.respond(
        f"{ctx.author.display_name} challenges {opponent.display_name} to a game of Tic-Tac-Toe!",
        view=view)

    # Create a link to the game message
    link_to_game = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{game_message.id}"

    # Send the DM with the link
    await opponent.send(
        f"{ctx.author.display_name} has challenged you to a game of Tic-Tac-Toe! [Click here to join the game]({link_to_game})"
    )


def setup(bot):
  bot.add_cog(TicTacToe(bot))

