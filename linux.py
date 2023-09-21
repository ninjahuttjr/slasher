import discord
from discord.commands import slash_command
from discord.ext import commands
import os
import subprocess

SSH_USER = "djpaintremodel"
SSH_HOST = "34.16.158.73"
# Ensure your private key is secure and has appropriate permissions
SSH_KEY_PATH = "./cogs/key.txt"


class LinuxCommands(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def execute_remote_command(self, command):
    cmd = ["ssh", "-i", SSH_KEY_PATH, f"{SSH_USER}@{SSH_HOST}", command]
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode(), err.decode()

  @slash_command(name='pwd')
  async def pwd(self, ctx):
    out, err = await self.execute_remote_command("pwd")
    await ctx.send(out if out else err)

  @slash_command(name='ls')
  async def ls(self, ctx, dir: str = ''):
    out, err = await self.execute_remote_command(f"ls {dir}")
    await ctx.send(out if out else err)

  @slash_command(name='cat')
  async def cat(self, ctx, file: str):
    out, err = await self.execute_remote_command(f"cat {file}")
    await ctx.send(out if out else err)

  @slash_command(name='whoami')
  async def whoami(self, ctx):
    out, err = await self.execute_remote_command("whoami")
    await ctx.send(out if out else err)


def setup(bot):
  bot.add_cog(LinuxCommands(bot))
