import discord
from discord.commands import slash_command
from discord.ext import commands
import os
import requests
from bs4 import BeautifulSoup


class WebScraper(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command(name='web')
  async def web_search(self, ctx, *, query):
    await ctx.defer()
    results = self.google_search(query)
    for res in results:
      embed = discord.Embed(title=res['title'],
                            url=res['link'],
                            color=discord.Color.blue())
      await ctx.send(embed=embed)

    # Provide a final response to the initial interaction to remove the "thinking" message
    await ctx.edit(content="Search results sent!")

  def google_search(self, query):
    base_url = "https://www.google.com/search?q={}"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(base_url.format(query), headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")
    search_results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
      anchor = g.find('a')
      title = g.find('h3').text
      link = anchor['href']
      search_results.append({"title": title, "link": link})

    # Save to file (without snippets)
    with open("./google_search_results.txt", "w", encoding="utf-8") as file:
      for res in search_results:
        file.write(f"Title: {res['title']}\nLink: {res['link']}\n\n")

    return search_results


def setup(bot):
  bot.add_cog(WebScraper(bot))
