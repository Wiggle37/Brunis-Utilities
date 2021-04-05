import discord
from discord.ext import commands

import sqlite3

class Vouch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('vouch.db')
        cursor = dbase.cursor()

def setup(client):
    client.add_cog(Vouch(client))