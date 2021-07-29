import discord
from discord.ext import commands

import aiohttp
import json
import time
import asyncio
import concurrent
import speedtest

from config import *
from buttons import *

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    @commands.command()
    async def test(self, ctx):
        await ctx.send(f'<t:{int((ctx.author.created_at.timestamp() - 1814400) + time.time())}:R>')

    @commands.command()
    async def testt(self, ctx):
        view = ChoseLockdown(ctx.author.id)
        await ctx.send('e', view=view)
        await view.wait()
        if view.value is None:
            return
        elif view.value == 0:
            return
        elif view.value == 1:
            return
        elif view.value == 2:
            return

def setup(bot):
    bot.add_cog(Testing(bot))