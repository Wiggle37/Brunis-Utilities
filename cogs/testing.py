import discord
from discord import role
from discord.ext import commands

import aiohttp
import json
import time
import asyncio
import concurrent
from discord.ext.commands.core import command
import speedtest
import aiosqlite
import motor
import motor.motor_asyncio
from datetime import datetime
import time

from config import *
from buttons import *

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.motor_session = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://mainHost:TStB72SYJGmte1MC@brunis-utilities.okced.mongodb.net/donations?retryWrites=true&w=majority')

def setup(bot):
    bot.add_cog(Testing(bot))