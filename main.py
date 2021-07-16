import discord
from discord.colour import Color
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv
import aiohttp
from datetime import datetime

from color import *

load_dotenv()
TOKEN = os.getenv("TOKEN")
    
bot = commands.Bot(
    command_prefix = ["b!", "B!", "b ", "B "],
    intents = discord.Intents.all(),
    case_insensitive = True,
    owner_ids = {531317158530121738, 824010269071507536,  737020572906684556},
)

# case insensitive help command for cogs 
bot._BotBase__cogs = commands.core._CaseInsensitiveDict()

# creates a global aiohttp session that can be used
async def aiohttp_session():
    bot.session = aiohttp.ClientSession()

async def load_extensions():
    await bot.wait_until_ready()
    print("\-/ Loading Cogs... \-/\n")
    
    # gets the path name and files in every directory
    # includes nested paths
    # only load if it"s in a directory called "cogs"
    for (dirpath, _, filenames) in os.walk("cogs"):

        # only load python files
        py_filenames = list(filter(lambda fn: fn.endswith(".py"), filenames))

        # loads each extension
        for fn in py_filenames:

            # prepares the extension to be loaded
            ext = dirpath.replace("\\", ".") + "." + fn[:-3]

            try:
                bot.load_extension(ext)
                print(f"{ext} loaded")
            
            except:
                print(f'{color.RED}There was an error loading {ext} please check the debug channel for more information{color.END}')

@bot.event
async def on_ready():
    print(
        f"{color.GREEN}\n /-\ Cogs Loaded /-\\{color.END}"
        f"{color.BLACK}\n==============================================\n{color.END}"
        f"{color.YELLOW}User: {bot.user}\n{color.END}"
        f"{color.YELLOW}ID: {bot.user.id}\n{color.END}"
        f"{color.YELLOW}Latency: {round(bot.latency * 1000, 2)}ms\n{color.END}"
        f"{color.YELLOW}Time: {datetime.utcnow()}\n{color.END}"
        f"{color.BLACK}==============================================\n{color.END}")

@tasks.loop(seconds = 60)
async def status():
    memberCount = sum(guild.member_count for guild in bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Over {memberCount} people"), status = discord.Status.idle)

@status.before_loop
async def bot_ready():
    await bot.wait_until_ready()

bot.loop.create_task(load_extensions())
bot.loop.create_task(aiohttp_session())
status.start()
bot.run(TOKEN)