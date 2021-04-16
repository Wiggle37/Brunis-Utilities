import discord
from discord.ext import commands

import sqlite3

class Strike(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Strike
    @commands.command()
    async def strike(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('strike.db')
        cursor = dbase.cursor()

        client = self.client

        user = member.id

        cursor.execute(f"SELECT strike FROM strikes WHERE user_id = '{member.id}'")
        result = cursor.fetchone()
        result = int(result[0])

        if result >= 2:
            pass

        else:
            strikes = 1

            cursor.execute("INSERT INTO strikes (user_id, strike) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET strike = strike + ?;", [user, strikes, strikes])

            cursor.execute(f"SELECT strike FROM strikes WHERE user_id = '{member.id}'")
            result = cursor.fetchone()
            result = (result[0])

            await ctx.send(f'{member} has been striked, this is strike number **{result}**')

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Strike(client))