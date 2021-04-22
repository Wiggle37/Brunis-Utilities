import discord
from discord.ext import commands

class Donations(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def donate(self, ctx):
        embed = discord.Embed(title='Donations', description='Donations are exepted, please dm <@765322777329664089> for more info', color=0x00ff00)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Donations(client))