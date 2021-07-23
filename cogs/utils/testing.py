import discord
from discord.ext import commands

from typing import List
import aiohttp

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        from config import CONFIG
        return await ctx.send(CONFIG["settings"])

def setup(bot):
    bot.add_cog(Testing(bot))