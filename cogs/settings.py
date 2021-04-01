import discord
from discord.ext import commands

class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def set_permissions(self, ctx, role: discord.Role):
        

def setup(client):
    client.add_cog(Settings(client))