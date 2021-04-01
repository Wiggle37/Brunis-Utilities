import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def announce(self, ctx, *, msg):
        client = self.client

        await client.get_channel(827293945003376650).send(msg)
        await ctx.send('Annoucement sent to <#827293945003376650>')

def setup(client):
    client.add_cog(Owner(client))