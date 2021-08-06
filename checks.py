import discord
from discord.ext import commands

import aiosqlite
import motor.motor_asyncio

from config import *

db = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://mainHost:TStB72SYJGmte1MC@brunis-utilities.okced.mongodb.net/donations?retryWrites=true&w=majority')
collection = db.guild_config

# Economy Checks
class economysettings:
    @staticmethod
    async def banned(user_id):
        async with aiosqlite.connect('settings.db') as dbase:
            cursor = await dbase.execute(f"SELECT ban FROM bans WHERE user_id = '{user_id}'")
            result = await cursor.fetchone()

        return result is not None

    @staticmethod
    def economycheck():
        async def predicate(ctx):
            return ctx.channel.id not in CONFIG["settings"]["economy"]["blacklistedchannels"] \
                and await economysettings.banned(ctx.author.id) is False
        return commands.check(predicate)

# Server Checks
class serverChecks:
    @staticmethod
    def merchants():
        async def predicate(ctx):
            return ctx.guild.id == 784491141022220309
        return commands.check(predicate)