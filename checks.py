import aiosqlite
from discord.ext import commands

from config import *

class economysettings:
    @staticmethod
    async def banned(user_id):
        dbase = await aiosqlite.connect('settings.db')
        cursor = await dbase.cursor()

        await cursor.execute(f"SELECT ban FROM bans WHERE user_id = '{user_id}'")
        result = await cursor.fetchone()

        await dbase.close()
        return result is not None

    @staticmethod
    def economycheck():
        async def predicate(ctx):
            return ctx.channel.id not in CONFIG["config"]["settings"]["blacklistedchannels"] \
                and await economysettings.banned(ctx.author.id) is False
        return commands.check(predicate)