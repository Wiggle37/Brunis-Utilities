import discord
from discord.ext import commands

import aiohttp
import json

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    

def setup(bot):
    bot.add_cog(Testing(bot))