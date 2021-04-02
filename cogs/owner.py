import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Announce
    @commands.command()
    async def announce(self, ctx, *, msg):
        client = self.client

        await client.get_channel(827293945003376650).send(msg)
        await client.get_channel(827293945003376650).send(f'\nMSG sent by: **{ctx.message.author}**')
        await ctx.send('Announcement sent to <#827293945003376650>')

    #Update
    @commands.command()
    async def update(self, ctx):
        pass

def setup(client):
    client.add_cog(Owner(client))