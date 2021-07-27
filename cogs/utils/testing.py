import discord
from discord.ext import commands

import aiohttp
import json
import time

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    @commands.command()
    async def test(self, ctx):
        await ctx.send(f'<t:{int((ctx.author.created_at.timestamp() - 1814400) + time.time())}:R>')

def setup(bot):
    bot.add_cog(Testing(bot))