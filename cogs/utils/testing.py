import discord
from discord.ext import commands

from typing import List
import aiohttp

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.author.send('🤡')

def setup(bot):
    bot.add_cog(Testing(bot))