import discord
from discord.ext import commands
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.conversations = {}  # To store conversation history for each user

  @commands.slash_command(name='chat')
  async def chat_with_gpt(self, ctx, *, user_input):
    await ctx.defer()
    user_id = ctx.author.id

    # Initialize conversation history if not exists
    if user_id not in self.conversations:
      self.conversations[user_id] = []

    # Append user's message to conversation history
    self.conversations[user_id].append({"role": "user", "content": user_input})

    # Send message to GPT-4 and get the response
    response = self.send_message_to_gpt(self.conversations[user_id])

    # Append GPT-4's message to conversation history
    self.conversations[user_id].append({
        "role": "assistant",
        "content": response
    })

    # Split the response into chunks of 2000 characters or less
    response_chunks = [
        response[i:i + 2000] for i in range(0, len(response), 2000)
    ]

    # Edit the deferred response to show the first chunk of GPT-4's response
    await ctx.edit(content=response_chunks[0])

    # Send the remaining chunks as separate messages
    for chunk in response_chunks[1:]:
      await ctx.send(chunk)

  def send_message_to_gpt(self, conversation):
    # Your logic to send message to GPT-4 and get the response
    # For example:
    response = openai.ChatCompletion.create(model="gpt-4",
                                            messages=conversation,
                                            max_tokens=850)
    print(response)  # Debugging line to print the full API response
    try:
      return response.choices[0].message['content'].strip()
    except AttributeError:
      return "An error occurred while processing the response."


def setup(bot):
  bot.add_cog(ChatGPT(bot))
