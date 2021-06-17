import discord
from discord.ext import commands
from discord.ext.commands.core import command

class Cog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        messages = await ctx.channel.history(limit=5).flatten()
        print(messages)

def setup(client):
    client.add_cog(Cog(client))