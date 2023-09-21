import discord
from discord.ext import commands

# List of admin role IDs
ADMIN_ROLE_IDS = [1152049468913496144, 1144682568264986695]


def is_admin(ctx):
  """Check if the member has any of the admin roles."""
  return any(role.id in ADMIN_ROLE_IDS for role in ctx.author.roles)


class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.check(is_admin)
  @commands.slash_command(
      name='clear',
      description="Clear a specified number of messages from the channel.")
  async def clear(self, ctx, amount: int):
    await ctx.defer()
    if amount < 1:
      await ctx.send("You must delete at least one message!")
      return
    await ctx.channel.purge(limit=amount + 1
                            )  # +1 to include the command message itself
    await ctx.send(f"Deleted {amount} messages!", delete_after=5
                   )  # This message will self-delete after 5 seconds

  @clear.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send(
          "You don't have the required permissions to use this command!")

  @commands.check(is_admin)
  @commands.slash_command(name='ban', description="Ban a specified user.")
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    await ctx.defer()
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send(
          "You don't have the required permissions to use this command!")

  @commands.check(is_admin)
  @commands.slash_command(name='kick', description="Kick a specified user.")
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    await ctx.defer()
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send(
          "You don't have the required permissions to use this command!")


def setup(bot):
  bot.add_cog(Moderation(bot))
