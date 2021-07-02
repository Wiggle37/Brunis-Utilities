import discord
from discord.ext import commands
import asyncio
import os
from discord.ext.commands.converter import clean_content
from dotenv import load_dotenv
from datetime import datetime
import sys

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(
    command_prefix=['b!', 'B!', 'b ', 'B '],
    intents=intents,
    case_insensitive=True,
    owner_ids = {531317158530121738, 824010269071507536, 784172569153503332}
    )

@client.event
async def on_ready():
    print(f'\n\-/ Loading... \-/\n')

    for folder in [f for f in os.listdir("./cogs") if f != "__pycache__"]:
        if folder.endswith(".py"):
            client.load_extension(f"cogs.{folder[:-3]}")
            print(f'cogs.{folder[:-3]} loaded')
        else:
            for file in [f for f in os.listdir(f"./cogs/{folder}") if f != "__pycache__"]:
                client.load_extension(f"cogs.{folder}.{file[:-3]}")
                print(f'cogs.{file[:-3]} loaded')

    await client.change_presence(status=discord.Status.dnd)
    print(f'\n==============================================\nUser: {client.user}\nID: {client.user.id}\nLatency: {int(client.latency * 1000)}\nTime: {datetime.utcnow()}\n==============================================\n')

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send('Restarting <a:loading:858913963005706270>')
    restart_bot()

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

@client.command()
@commands.is_owner()
async def refresh(ctx):
    for folder in [f for f in os.listdir("./cogs") if f != "__pycache__"]:
        if folder.endswith(".py"):
            client.unload_extension(f'cogs.{folder[:-3]}')
            client.load_extension(f"cogs.{folder[:-3]}")
        else:
            for file in [f for f in os.listdir(f"./cogs/{folder}") if f != "__pycache__"]:
                client.unload_extension(f"cogs.{folder}.{file[:-3]}")
                client.load_extension(f"cogs.{folder}.{file[:-3]}")
    await ctx.send('Refreshed the whole bot')

async def status():
    await client.wait_until_ready()
    while True:
        memberCount = sum([guild.member_count for guild in client.guilds])
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over {memberCount} people'))

        await asyncio.sleep(30)

client.loop.create_task(status())

client.run(TOKEN)