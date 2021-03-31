###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import os
from dotenv import load_dotenv

import sqlite3

###Intents###
intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(
    shard_count=3,
    command_prefix='b!',
    intents=intents,
    case_insensitive=True,
    )
client.remove_command('help')

###Help###
@client.command()
async def help(ctx, cog=None):
    help_embed = discord.Embed(title='Brunis Utilities', description='This bot is for [](Dank Merchants)', color=0x00ff00)
    await ctx.send(embed=embed)

###On Ready###
@client.event
async def on_ready():
    print('Bot Online!')

#Dono Check

    
###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)