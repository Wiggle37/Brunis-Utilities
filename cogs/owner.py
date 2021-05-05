import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Announce
    @commands.command()
    @commands.is_owner()
    async def announce(self, ctx, *, msg):
        client = self.client

        await client.get_channel(827293945003376650).send(msg)
        await client.get_channel(827293945003376650).send(f'\nMSG sent by: **{ctx.message.author}**')
        await ctx.send('Announcement sent to <#827293945003376650>')

    @announce.error
    async def announce_error(self, ctx, error):
        await ctx.send('Only Wiggle can use this command')

def setup(client):
    client.add_cog(Owner(client))