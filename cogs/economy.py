import discord
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bal', 'money'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member=None):
        pass

def setup(client):
    client.add_cog(Economy(client))