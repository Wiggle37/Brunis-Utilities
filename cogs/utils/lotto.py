import discord
from discord.ext import commands
import sqlite3

class Lottery(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Start Lottery
    @commands.command(name='startlottery')
    async def startlottery(self, ctx, name):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        if len(name.split()) > 1:
            return await ctx.send('You can only have a one word lottery name.')

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{name.lower()}" (
	                "user_id"	INTEGER UNIQUE,
	                "tickets"	INTEGER DEFAULT 0
        );""")

        await ctx.send(f'**Lottery Made With The Name {name}**')

        dbase.commit()
        dbase.close()

    #End Lottery
    @commands.command(name='endlottery')
    async def endlottery(self, ctx, name):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #Add Tickets
    @commands.command(name='addticket')
    async def addticket(self, ctx, member: discord.Member, amount: int=1):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #Remove Tickets
    @commands.command(name='removeticket')
    async def removeticket(self, ctx, member: discord.Member, amount: int=1):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #View Tickets For Member
    @commands.command()
    async def tickets(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #View All Tickets
    @commands.command()
    async def viewlotto(self, ctx, lottery):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Lottery(client))