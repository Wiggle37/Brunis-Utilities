import discord
from discord.ext import commands

import sqlite3

class Vouch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def vouch(self, ctx, member: discord.Member=None):
        

def setup(client):
    client.add_cog(Vouch(client))