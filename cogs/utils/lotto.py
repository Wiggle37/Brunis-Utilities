import discord
from discord.ext import commands
import sqlite3

class Lottery(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Start Lottery
    @commands.command(name='startlottery')
    async def startlottery(self, ctx, name):
        pass

    #End Lottery
    @commands.command(name='endlottery')
    async def endlottery(self, ctx, name):
        pass

    #Add Tickets
    @commands.command(name='addticket')
    async def addticket(self, ctx, member: discord.Member, amount: int=1):
        pass

    #Remove Tickets
    @commands.command(name='removeticket')
    async def removeticket(self, ctx, member: discord.Member, amount: int=1):
        pass

def setup(client):
    client.add_cog(Lottery(client))