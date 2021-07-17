import discord
from discord.ext import commands

from config import *

class DmCommands(commands.Cog, name='dm', description='Commands that can only be used in dms'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await message.reply(f'Hello! I am {self.bot.user}, run the command `b!dm` to get a list of dm commands')

def setup(bot):
    bot.add_cog(DmCommands(bot))