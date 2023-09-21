import discord
from discord.ext import commands
import random

# Constants
GUILD_1 = 1066826355444027412
GUILD_2 = 759187011407052820
GUESS_COMMAND_ID_GUILD_1 = 1149854464631636158
GUESS_COMMAND_ID_GUILD_2 = 1149854466045132850  # Replace with the actual command ID for this guild

SOVLE_COMMAND_ID_GUILD_1 = 1149857115985416283
SOVLE_COMMAND_ID_GUILD_2 = 1149857119504433352


class Hangman(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.words = [
        'elephant', 'giraffe', 'kangaroo', 'crocodile', 'platypus', 'squirrel',
        'dolphin', 'penguin', 'flamingo', 'gorilla', 'jaguar', 'koala',
        'lemur', 'meerkat', 'octopus', 'ostrich', 'panda', 'peacock',
        'porcupine', 'rhinoceros', 'seahorse', 'tiger', 'turtle', 'vulture',
        'walrus', 'weasel', 'wombat', 'zebra', 'lynx', 'badger'
    ]
    self.games = {}

  @commands.slash_command(guild_ids=[GUILD_1, GUILD_2],
                          name='hangman',
                          description='Play Hangman')
  async def start_hangman(self, ctx: discord.ApplicationContext):
    if ctx.author.id in self.games:
      await ctx.respond("You are already in a game!")
      return

    # Determine the command ID based on the guild
    if ctx.guild_id == GUILD_1:
      guess_command_id = GUESS_COMMAND_ID_GUILD_1
    elif ctx.guild_id == GUILD_2:
      guess_command_id = GUESS_COMMAND_ID_GUILD_2
    else:
      guess_command_id = GUESS_COMMAND_ID_GUILD_1  # Default to GUILD_1's command ID

    word = random.choice(self.words)
    self.games[ctx.author.id] = {
        'word': word,
        'guesses': set(),
        'attempts': 6,
        'guess_command_id': guess_command_id
    }

    embed = discord.Embed(
        title="Welcome to Hangman!",
        description=
        f"You have 6 attempts. The word has {len(word)} letters. Type or click </guess:{guess_command_id}> to make a guess."
    )
    await ctx.respond(embed=embed, ephemeral=False)  # Send the initial embed

    # Fetch the last message sent in the channel (which should be the embed)
    message = await ctx.channel.fetch_message(ctx.channel.last_message_id)
    self.games[ctx.author.id]['message'] = message  # Store the Message object

  @commands.slash_command(guild_ids=[GUILD_1, GUILD_2],
                          name='guess',
                          description='Guess a letter')
  async def guess_letter(self, ctx: discord.ApplicationContext, letter: str):
    if ctx.author.id not in self.games:
      await ctx.respond(
          "You are not in a game. Start a new game with `/hangman`.",
          ephemeral=True)
      return

    game = self.games[ctx.author.id]
    guess_command_id = game['guess_command_id']

    if letter in game['guesses']:
      await ctx.respond(f"You've already guessed '{letter}'.", ephemeral=True)
      return

    game['guesses'].add(letter)  # Using add() for sets
    if letter not in game['word']:
      game['attempts'] -= 1

    # Construct the display_word
    display_word = ''.join(
        [l if l in game['guesses'] else '_' for l in game['word']])

    embed = discord.Embed(
        title="Hangman Game",
        description=
        f"`{display_word}` | Attempts left: {game['attempts']} | To guess type or click </guess:{guess_command_id}> or solve with </solve:{guess_command_id}>"
    )
    embed.add_field(name="Guessed Letters", value=", ".join(game['guesses']))

    if '_' not in display_word:
      embed.title = "Congratulations!"
      embed.description = f"You've guessed the word: {game['word']}"
      await game['message'].edit(embed=embed)
      del self.games[ctx.author.id]
      await ctx.respond("You've won!", ephemeral=True)
      return

    if game['attempts'] == 0:
      embed.add_field(name="Game Over!", value=f"The word was: {game['word']}")
      await game['message'].edit(embed=embed)
      del self.games[ctx.author.id]
      await ctx.respond("Game over!", ephemeral=True)
      return

    await game['message'].edit(embed=embed)
    await ctx.respond("Guess received", delete_after=1.99)  # Acknowledge

  @commands.slash_command(guild_ids=[GUILD_1, GUILD_2],
                          name='solve',
                          description='Attempt to solve the entire word')
  async def solve_word(self, ctx: discord.ApplicationContext, solution: str):
    if ctx.author.id not in self.games:
      await ctx.respond(
          "You are not in a game. Start a new game with `/hangman`.",
          ephemeral=True)
      return

    game = self.games[ctx.author.id]
    guess_command_id = game[
        'guess_command_id']  # Fetch the guess_command_id from the game data
    embed = discord.Embed()

    if solution == game['word']:
      embed.title = "Congratulations!"
      embed.description = f"You've correctly solved the word: {game['word']}"
      await game['message'].edit(embed=embed)
      del self.games[ctx.author.id]
      await ctx.respond("You've won!", ephemeral=True)
    else:
      game['attempts'] -= 1
      embed.title = "Hangman Game"
      display_word = ''.join(
          [l if l in game['guesses'] else '_' for l in game['word']])
      embed.description = f"`{display_word}` | Attempts left: {game['attempts']} | Type or click </guess:{guess_command_id}> to make another guess."
      embed.add_field(name="Guessed Letters", value=", ".join(game['guesses']))

      if game['attempts'] == 0:
        embed.add_field(name="Game Over!",
                        value=f"The word was: {game['word']}")
        await game['message'].edit(embed=embed)
        del self.games[ctx.author.id]
        await ctx.respond("Game over!", ephemeral=True)
        return

      await game['message'].edit(embed=embed)
      await ctx.respond(
          f"Incorrect solution. You have {game['attempts']} attempts left.",
          ephemeral=True)


def setup(bot):
  bot.add_cog(Hangman(bot))
