import aiosqlite
from discord.ext import commands

from config import *

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
            return ctx.channel.id not in CONFIG["config"]["settings"]["blacklistedchannels"] \
                and await economysettings.banned(ctx.author.id) is False
        return commands.check(predicate)