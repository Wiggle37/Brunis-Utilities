###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import asyncio

import os
from dotenv import load_dotenv

###Bot###
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
    print(f'Bot is now online!\n--------------------\nUser: {client.user}\nID: {client.user.id}')

###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'cog.{filename[:-3]} loaded')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded **{extension}**')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded **{extension}**')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded **{extension}**')

async def status():
    await client.wait_until_ready()
    while True:
        memberCount = sum([guild.member_count for guild in client.guilds])
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over {memberCount} people'))

        await asyncio.sleep(30)

client.loop.create_task(status())

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('BOT_TOKEN')
client.run(Bot_Token)