import discord
from discord.ext import commands

from config import *

class Afk(commands.Cog, name='AFK'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='afk')
    async def afk(self, ctx, *, reason):
        await ctx.send(f'{ctx.author.mention}: I have marked you afk for "{reason}"')

def setup(bot):
    bot.add_cog(Afk(bot))