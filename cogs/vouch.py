import discord
from discord.ext import commands

import sqlite3

class Vouch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message, member: discord.Member=None):
        if message.content.startswith('+1'):
            if message.channel.id == 815057225378431056 or message.channel.id == 784491141022220312:
                dbase = sqlite3.connect('vouch.db')
                cursor = dbase.cursor()

                user = (f'{member}')
                amount = 1

                cursor.execute("INSERT INTO vouches (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

                dbase.commit()
                dbase.close()

def setup(client):
    client.add_cog(Vouch(client))