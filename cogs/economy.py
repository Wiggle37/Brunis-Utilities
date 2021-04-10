import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import sqlite3

import random

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Money Add
    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def on_message(self, message):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT user_id FROM balance WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        user = message.author.id


        if result is None:
            balance = 0

            cursor.execute("INSERT INTO balance (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance = ?;", [user, balance, balance])

        else:
            balance = 10

            cursor.execute("INSERT INTO balance (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, balance, balance])

        dbase.commit()
        dbase.close()

    #Balance
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member is None:
            cursor.execute(f"SELECT balance FROM balance WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])
            result = ('{:,}'.format(result))

            bal_embed = discord.Embed(title=f"{ctx.message.author}'s Balance", description=f'{result}', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        else:
            cursor.execute(f"SELECT balance FROM balance WHERE user_id = '{member.id}'")
            result = cursor.fetchone()
            result = (result[0])
            result = ('{:,}'.format(result))

            bal_embed = discord.Embed(title=f"{member}'s Balance", description=f'{result}', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        dbase.commit()
        dbase.close()

    #Shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx, item=None):
        #Page 1
        if item is None or item == '1':
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<a:omega:791410419624443934> **1 Week Auto Reaction** - <:dankmerchants:829809749058650152> 75,000\n\n<a:premium:797290098189664256> **1 Week Server Premium** - <:dankmerchants:829809749058650152> 100,000\n\n<a:bypass:829822077795958785> **1 Week Giveaway Bypass** <:dankmerchants:829809749058650152> 100,000\n\n🏡 **1 Week Custom Channel** - <:dankmerchants:829809749058650152> 250,000\n\n<a:blob:829822719372951592> **1 Week Custom Role** - <:dankmerchants:829809749058650152> 250,000', color=0x00ff00)
            embed.set_footer(text='Page 1-2')
            await ctx.send(embed=embed)

        #Page 2
        if item == '2':
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<:woodbox:830211928595890206> **Wood Loot Box** - <:dankmerchants:829809749058650152> 50,000\n\n<:ironbox:830197241934512188> **Iron Loot Box** - <:dankmerchants:829809749058650152> 100,000\n\n<:goldbox:830197220405805147> **Gold Loot Box** - <:dankmerchants:829809749058650152> 250,000\n\n<:diamondbox:830197220007477259> **Diamond Loot Box** - <:dankmerchants:829809749058650152> 500,000\n\n<:emeraldbox:830216613755486229> **Emerald Loot Box** - <:dankmerchants:829809749058650152> 1,000,000', color=0x00ff00)
            embed.set_footer(text='Page 2-2')
            await ctx.send(embed=embed)

        #Reaction
        if item == 'reaction':
            embed = discord.Embed(title='1 Week Auto Reaction', description='When your name is pinged make the bot auto react.', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **75,000**')
            await ctx.send(embed=embed)

    #Beg
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beg(self, ctx):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

        names = [
            'Carl',
            'Jimmy',
            'Bob',
            'Lily',
            'Gerald',
            'Joe',
            'Karal'
        ]

        amount = random.randint(100, 1000)

        print(amount)

        cursor.execute("INSERT INTO balance (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

        amount = ('{:,}'.format(amount))
        await ctx.send(f'{random.choice(names)} Gave you <:dankmerchants:829809749058650152> **{amount}**!')

        dbase.commit()
        dbase.close()

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))