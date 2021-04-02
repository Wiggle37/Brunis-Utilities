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

###On Ready###
@client.event
async def on_ready():
    print('Bot Online!')

    dbase = sqlite3.connect('bruni.db')
    cursor = dbase.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS "gaw_dono_logs" (
	"guild_id"	INTEGER,
	"user_id"	INTEGER UNIQUE,
	"amount"	INTEGER DEFAULT 0
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS "heist_dono_logs" (
	"guild_id"	INTEGER,
	"user_id"	INTEGER UNIQUE,
	"amount"	INTEGER DEFAULT 0
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS "event_dono_logs" (
	"guild_id"	INTEGER,
	"user_id"	INTEGER UNIQUE,
	"amount"	INTEGER DEFAULT 0
    )""")

    dbase.commit()
    dbase.close()
    
###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)