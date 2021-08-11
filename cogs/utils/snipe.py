import discord
import asyncio
import sqlite3
from discord.ext import commands

snipe_message_author = {}
snipe_message_content = {}

class snipe(commands.Cog):
  def __init__(self, client):
    self.client=client
    self.snipe_message_content = None
    self.snipe_message_author = None

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
  
  @commands.command()
  async def snipe(self, ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(title = f"Last deleted message in {channel}", description = snipe_message_content[channel.id], color = 0xf5ff88)
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"There are no recently deleted messages in {channel.mention}")

def setup(client):
  client.add_cog(snipe(client))