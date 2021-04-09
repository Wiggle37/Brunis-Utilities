import discord
from discord.ext import commands

import sqlite3

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #Balance
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member is None:
            bal_embed = discord.Embed(title=f"{ctx.message.author}'s Balance", description='Description', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        else:
            bal_embed = discord.Embed(title=f"{member}'s Balance", description='Description', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        dbase.commit()
        dbase.close()

    #Shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx, page: int=None):
        if page is None or page = 1:
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<a:omega:791410419624443934> **1 Week Auto Reaction** - <:dankmerchants:829809749058650152> 75,000\n\n<a:premium:797290098189664256> **1 Week Server Premium** - <:dankmerchants:829809749058650152> 100,000\n\n<a:bypass:829822077795958785> **1 Week Giveaway Bypass** <:dankmerchants:829809749058650152> 100,000\n\n🏡 **1 Week Custom Channel** - <:dankmerchants:829809749058650152> 250,000\n\n<a:blob:829822719372951592> **1 Week Custom Role** - <:dankmerchants:829809749058650152> 250,000', color=0x00ff00)
            await ctx.send(embed=embed)

        if page = 2:
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n', color=0x00ff00)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))