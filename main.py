###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import asyncio

import os
from dotenv import load_dotenv

###Intents###
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    command_prefix=['b!', 'B!'],
    intents=intents,
    case_insensitive=True,
    )
client.remove_command('help')

###On Ready###
@client.event
async def on_ready():
    print(f'Bot is now online!\n---BOT INFO---\n--------------------\nUser: {client.user}\nID: {client.user.id}')

###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

async def status():
    await client.wait_until_ready()
    while True:
        guildCount = len(client.guilds)
        memberCount = sum([guild.member_count for guild in client.guilds])
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f'{memberCount} members in {guildCount} servers'))

        await asyncio.sleep(60)

client.loop.create_task(status())

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)