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
client = commands.Bot(
    command_prefix='b!',
    intents=intents,
    case_insensitive=True,
    )
client.remove_command('help')

###On Ready###
@client.event
async def on_ready():
    print(f'{client.user} is online!')

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over Dank Merchants'))

###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        
###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)