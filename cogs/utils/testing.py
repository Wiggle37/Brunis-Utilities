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

    @commands.command()
    @commands.is_owner()
    async def friskygae(self, ctx):
        channel = self.bot.get_channel(784493280498155542)
        message = await channel.fetch_message(869087109057761301)
        users = []
        for reaction in message.reactions:
            async for user in reaction.users():
                users.append(f'{user.mention}')
        
        split = [users[i:i+1755] for i in range(0, len(users), 1755)]
        for info in split:
            await ctx.send(f"{info}")

def setup(bot):
    bot.add_cog(Testing(bot))