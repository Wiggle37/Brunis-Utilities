###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import asyncio

import os
from dotenv import load_dotenv

import random

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
        memberCount = sum([guild.member_count for guild in client.guilds])
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f'over {memberCount} people'))

        await asyncio.sleep(60)

client.loop.create_task(status())

@client.command()
async def pp(ctx):
    sizes = [
            '0 in. \n8D',
            '1 in. \n8=D',
            '2 in. \n8==D',
            '3 in. \n8===D',
            '4 in. \n8====D',
            '5 in. \n8=====D',
            '6 in. \n8======D',
            '7 in. \n8=======D',
            '8 in. \n8========D',
            '9 in. \n8=========D',
            '10 in. \n8=========D',
            '11 in. \n8==========D',
            '12 in. \n8===========D'
        ]

    size = f'{random.choice(sizes)}'

    pp_embed = discord.Embed(title=f'{ctx.message.author}s pp', description=size, color=0x00ff00)
    await ctx.send(embed=pp_embed)

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)