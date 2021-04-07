import discord
from discord.ext import commands

import sqlite3

class Vouch(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Vouch
    @commands.command(aliases=['v'])
    async def vouch(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('vouch.db')
        cursor = dbase.cursor()

        user = (f'{member}')
        amount = 1

        cursor.execute("INSERT INTO vouches (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Vouch(client))