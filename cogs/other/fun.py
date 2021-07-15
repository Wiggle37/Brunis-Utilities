from discord.ext import commands
import http
import asyncio

class Fun(commands.Cog, name='fun', description='Some fun commands'):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Fun(bot))