import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import asyncio

import sqlite3

import random

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
    DB Adder
    '''
    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def on_message(self, message):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        user = message.author.id

        if result is None:
            balance = 500
            amount = 0

            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance = ?;", [user, balance, balance])
            cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox = ?;", [user, amount, amount])
            cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut = ?;", [user, amount, amount])
            cursor.execute("INSERT INTO items (user_id, ducks) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ducks = ducks = ?;", [user, amount, amount])

        dbase.commit()
        dbase.close()

    '''
    General
    '''
    #Balance
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member is None:
            cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()

            user = ctx.author.id

            if result is None:
                balance = 0

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance = ?;", [user, balance, balance])

            cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])
            result = ('{:,}'.format(result))

            bal_embed = discord.Embed(title=f"{ctx.message.author}'s Balance", description=f'**Balance:**\n<:dankmerchants:829809749058650152> {result}', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        else:
            cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{member.id}'")
            result = cursor.fetchone()

            user = member.id

            if result is None:
                balance = 0

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance = ?;", [user, balance, balance])

            cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{member.id}'")
            result = cursor.fetchone()
            result = (result[0])
            result = ('{:,}'.format(result))

            bal_embed = discord.Embed(title=f"{member}'s Balance", description=f'**Balance:**\n<:dankmerchants:829809749058650152> {result}', color=0x00ff00)
            await ctx.send(embed=bal_embed)

        dbase.commit()
        dbase.close()

    #Inventory
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, page=None, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member == None:
            
            if page == '1' or page == None:
                cursor.execute(f"SELECT woodbox FROM boxes WHERE user_id = '{ctx.author.id}'")
                woodbox = cursor.fetchone()
                woodbox = (woodbox[0])

                cursor.execute(f"SELECT ironbox FROM boxes WHERE user_id = '{ctx.author.id}'")
                ironbox = cursor.fetchone()
                ironbox = (ironbox[0])

                cursor.execute(f"SELECT goldbox FROM boxes WHERE user_id = '{ctx.author.id}'")
                goldbox = cursor.fetchone()
                goldbox = (goldbox[0])

                cursor.execute(f"SELECT diamondbox FROM boxes WHERE user_id = '{ctx.author.id}'")
                diamondbox = cursor.fetchone()
                diamondbox = (diamondbox[0])

                cursor.execute(f"SELECT emeraldbox FROM boxes WHERE user_id = '{ctx.author.id}'")
                emeraldbox = cursor.fetchone()
                emeraldbox = (emeraldbox[0])

                embed = discord.Embed(title=f'{ctx.author}s Inventory', description='Loot Boxes', color=0x00ff00)
                embed.add_field(name=f'<:woodbox:830211928595890206> __Wooden Box__', value=f'**{woodbox}** owned', inline=False)
                embed.add_field(name=f'<:ironbox:830197241934512188> __Iron Box__', value=f'**{ironbox}** owned', inline=False)
                embed.add_field(name=f'<:goldbox:830197220405805147> __Gold Box__', value=f'**{goldbox}** owned', inline=False)
                embed.add_field(name=f'<:diamondbox:830197220007477259> __Diamond Box__', value=f'**{diamondbox}** owned', inline=False)
                embed.add_field(name=f'<:emeraldbox:830216613755486229> __Emerald Box__', value=f'**{emeraldbox}** owned', inline=False)
                embed.set_footer(text='Page 1-2')
                await ctx.send(embed=embed)

            if page == '2':
                cursor.execute(f"SELECT doughnut FROM multis WHERE user_id = '{ctx.author.id}'")
                doughnut = cursor.fetchone()
                doughnut = (doughnut[0])

                cursor.execute(f"SELECT brunisbackpack FROM multis WHERE user_id = '{ctx.author.id}'")
                backpack = cursor.fetchone()
                backpack = (backpack[0])

                embed = discord.Embed(title=f'{ctx.author}s Inventory', description='Multipliers', color=0x00ff00)
                embed.add_field(name=f'<:doughnut:831895771442839552> __Doughnut 5%__', value=f'**{doughnut}** owned', inline=False)
                embed.add_field(name='<:brunisbackpack:834948572826828830> __Brunis Backpack 10%__', value=f'**{backpack}** owned', inline=False)
                embed.set_footer(text='Page 2-2')
                await ctx.send(embed=embed)
            
        else:
            if page == '1' or page == None:
                cursor.execute(f"SELECT woodbox FROM boxes WHERE user_id = '{member.id}'")
                woodbox = cursor.fetchone()
                woodbox = (woodbox[0])

                cursor.execute(f"SELECT ironbox FROM boxes WHERE user_id = '{member.id}'")
                ironbox = cursor.fetchone()
                ironbox = (ironbox[0])

                cursor.execute(f"SELECT goldbox FROM boxes WHERE user_id = '{member.id}'")
                goldbox = cursor.fetchone()
                goldbox = (goldbox[0])

                cursor.execute(f"SELECT diamondbox FROM boxes WHERE user_id = '{member.id}'")
                diamondbox = cursor.fetchone()
                diamondbox = (diamondbox[0])

                cursor.execute(f"SELECT emeraldbox FROM boxes WHERE user_id = '{member.id}'")
                emeraldbox = cursor.fetchone()
                emeraldbox = (emeraldbox[0])

                embed = discord.Embed(title=f'{member}s Inventory', description='Loot Boxes', color=0x00ff00)
                embed.add_field(name=f'<:woodbox:830211928595890206> __Wooden Box__', value=f'**{woodbox}** owned', inline=False)
                embed.add_field(name=f'<:ironbox:830197241934512188> __Iron Box__', value=f'**{ironbox}** owned', inline=False)
                embed.add_field(name=f'<:goldbox:830197220405805147> __Gold Box__', value=f'**{goldbox}** owned', inline=False)
                embed.add_field(name=f'<:diamondbox:830197220007477259> __Diamond Box__', value=f'**{diamondbox}** owned', inline=False)
                embed.add_field(name=f'<:emeraldbox:830216613755486229> __Emerald Box__', value=f'**{emeraldbox}** owned', inline=False)
                embed.set_footer(text='Page 1-2')
                await ctx.send(embed=embed)

            if page == '2':
                cursor.execute(f"SELECT doughnut FROM multis WHERE user_id = '{member.id}'")
                doughnut = cursor.fetchone()
                doughnut = (doughnut[0])

                cursor.execute(f"SELECT brunisbackpack FROM multis WHERE user_id = '{member.id}'")
                backpack = cursor.fetchone()
                backpack = (backpack[0])

                embed = discord.Embed(title=f'{member.id}s Inventory', description='Multipliers', color=0x00ff00)
                embed.add_field(name=f'<:doughnut:831895771442839552> __Doughnut 5%__', value=f'**{doughnut}** owned', inline=False)
                embed.add_field(name='<:brunisbackpack:834948572826828830> __Brunis Backpack 10%__', value=f'**{backpack}** owned', inline=False)
                embed.set_footer(text='Page 2-2')
                await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    #Shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx, item=None):
        #Page 1
        if item == '1' or item is None:
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<:woodbox:830211928595890206> **Wood Loot Box** - <:dankmerchants:829809749058650152> 50,000\n\n<:ironbox:830197241934512188> **Iron Loot Box** - <:dankmerchants:829809749058650152> 100,000\n\n<:goldbox:830197220405805147> **Gold Loot Box** - <:dankmerchants:829809749058650152> 250,000\n\n<:diamondbox:830197220007477259> **Diamond Loot Box** - <:dankmerchants:829809749058650152> 500,000\n\n<:emeraldbox:830216613755486229> **Emerald Loot Box** - <:dankmerchants:829809749058650152> 1,000,000', color=0x00ff00)
            embed.set_footer(text='Page 2-2')
            await ctx.send(embed=embed)
        '''
        Items
        '''
        #Ducc
        if item == 'ducc' or item == 'duck':
            embed = discord.Embed(title='Duck', description='Its a duck that happens to be pretty powerful and annoying...', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/784491141022220312/830801553714577468/ducc.png')
            embed.add_field(name='Price:', value='Item Not Purchasable')
            await ctx.send(embed=embed)
        #Donut
        if item == 'doughnut' or item == 'donut':
            embed = discord.Embed(title='Dount', description='A dount that happens to give you a 5% multi cap of 25%', color=0xCDD319)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/831895771442839552.png?v=1')
            embed.add_field(name='Price:', value='Item Not Purchasable')
            await ctx.send(embed=embed)
        '''
        Boxes
        '''
        #Wooden Box
        if item == 'wood' or item == 'wooden':
            embed = discord.Embed(title='Wooden Box', description='A basic wooden box that could find you some loot', color=0x6C6C6C)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830211928595890206.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **50,000**')
            await ctx.send(embed=embed)
        #Iron Box
        if item == 'iron':
            embed = discord.Embed(title='Iron Box', description='A solid iron box probally has some good stuff in it', color=0x6DEA33)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197241934512188.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)
        #Gold Box
        if item == 'gold':
            embed = discord.Embed(title='Gold Box', description='A solid gold box that must have good loot', color=0x142DE8)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220405805147.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **250,000**')
            await ctx.send(embed=embed)
        #Diamond Box
        if item == 'diamond':
            embed = discord.Embed(title='Diamond Box', description='A solid diamond box that is bound to have good loot', color=0x770889)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220007477259.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **500,000**')
            await ctx.send(embed=embed)
        #Emerald Box
        if item == 'emerald':
            embed = discord.Embed(title='Emerald Box', description='The best box of them all that will have the best loot', color=0xEABB33)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830216613755486229.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **1,000,000**')
            await ctx.send(embed=embed)

    '''
    Buying Command
    '''
    @commands.command()
    async def buy(self, ctx, item=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        client = self.client
        member = ctx.author
        user = ctx.author.id

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        bal = (result[0])

        if item == None:
            await ctx.send('You actully have to name a item to buy it (0)_(0)')
        '''
        BOXES
        '''
        #Wooden Box
        if item == 'wooden' or item == 'wood':
            if bal >= 50000:
                amount = 50000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [user, box, box])

                await ctx.send('Enjoy your wooden box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Iron Box
        if item == 'iron':
            if bal >= 100000:
                amount = 100000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox + ?;", [user, box, box])

                await ctx.send('Enjoy your iron box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Gold Box
        if item == 'gold':
            if bal >= 250000:
                amount = 250000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox + ?;", [user, box, box])

                await ctx.send('Enjoy your gold box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Diamond Box
        if item == 'diamond':
            if bal >= 500000:
                amount = 500000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox + ?;", [user, box, box])

                await ctx.send('Enjoy your diamond box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Emerald Box
        if item == 'emerald':
            if bal >= 1000000:
                    amount = 1000000
                    box = 1
                    cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox + ?;", [user, box, box])

                    await ctx.send('Enjoy your emerald box')

            else:
                    await ctx.send('You dont have enough money to buy that!')

        dbase.commit()
        dbase.close()
    '''
    Using Items
    '''
    @commands.command()
    async def use(self, ctx, item=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

        selection = [
            'yes',
            'no'
        ]

        if item == None:
            await ctx.send('You have to give an item to use (0)_(0)')

        #Wooden Box
        if item == 'wooden' or item == 'wood':
            cursor.execute(f"SELECT woodbox FROM boxes WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1

                cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox - ?;", [user, box, box])
                
                coins = random.randint(25000, 50000)
                appleamount = random.randint(0, 5)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples: `{appleamount}`***')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Iron Box
        if item == 'iron':
            cursor.execute(f"SELECT ironbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO economy (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox - ?;", [user, box, box])

                coins = random.randint(50000, 100000)
                appleamount = random.randint(0, 10)
                duckamount = random.randint(1, 5)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Gold Box
        if item == 'gold':
            cursor.execute(f"SELECT goldbox FROM boxes WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox - ?;", [user, box, box])

                coins = random.randint(100000, 250000)
                appleamount = random.randint(0, 15)
                duckamount = random.randint(1, 10)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Diamond Box
        if item == 'diamond':
            cursor.execute(f"SELECT diamondbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox - ?;", [user, box, box])

                coins = random.randint(250000, 500000)
                appleamount = random.randint(1, 25)
                duckamount = random.randint(1, 25)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Emerald Box
        if item == 'emerald':
            cursor.execute(f"SELECT emeraldbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox - ?;", [user, box, box])

                coins = random.randint(500000, 1000000)
                appleamount = random.randint(1, 50)
                duckamount = random.randint(1, 10)
                donutamount = random.randint(0, 1)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])
                cursor.execute("INSERT INTO multi (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [user, donutamount, donutamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`\n***Donuts:*** `{donutamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        dbase.commit()
        dbase.close()

    '''
    Giving
    '''

    #Give
    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member == None:
            await ctx.reply('You actully have to give stuff to someone')

        else:
            if amount < 0:
                await ctx.send('Dont even try me')

            else:
                user = ctx.author.id
                member_id = member.id

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

                channel = await member.create_dm()
            
                dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\nYou got <:dankmerchants:829809749058650152> **{amount}** from {ctx.message.author}', color=0x00ff00)
                await channel.send(embed=dm_embed)

                await ctx.send(f'{ctx.author.mention} you gave **{member}** <:dankmerchants:829809749058650152> **{amount}**')

        dbase.commit()
        dbase.close()

    #Gift
    @commands.command()
    async def gift(self, ctx, amount: int=None, item=None, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        member_id = member.id
        user = ctx.author.id

        if member == None:
            await ctx.reply('You actully have to give stuff to someone')

        else:
            if amount < 0:
                await ctx.send('Dont even try me')

            else:
                if item == 'wood' or item == 'wooden' or item == 'woo':
                    cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:woodbox:830211928595890206> wooden box(es)', color=0x00ff00)
                    await channel.send(embed=dm_embed)
                    
                    await ctx.send(f'You gave **{member}** {amount} wooden boxe(es) <:woodbox:830211928595890206>')

                if item == 'iron' or item == 'iro':
                    cursor.execute("INSERT INTO boxes (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:ironbox:830197241934512188> iron box(es)', color=0x00ff00)
                    await channel.send(embed=dm_embed)
                    

                    await ctx.send(f'You gave **{member}** {amount} iron box(es) <:ironbox:830197241934512188>')


                if item == 'gold' or item == 'gol':
                    cursor.execute("INSERT INTO boxes (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:goldbox:830197220405805147> gold box(es)', color=0x00ff00)
                    await channel.send(embed=dm_embed)

                    await ctx.send(f'You gave **{member} {amount} gold box(es) <:goldbox:830197220405805147>')

                if item == 'diamond' or item == 'dia':
                    cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:diamondbox:830197220007477259> diamond box(es)', color=0x00ff00)
                    await channel.send(embed=dm_embed)

                    await ctx.send(f'You gave **{member} {amount} diamond box(es) <:diamondbox:830197220007477259>')

                if item == 'emerald' or item == 'eme':
                    cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:emeraldbox:830216613755486229> emerald box(es)', color=0x00ff00)
                    await channel.send(embed=dm_embed)

                    await ctx.send(f'You gave **{member}** {amount} emerald box(es) <:emeraldbox:830216613755486229>')

                if item == 'donut' or item == 'doughnut' or item == 'dough' or item == 'don':
                    cursor.execute("INSERT INTO boxes (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO boxes (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [member_id, amount, amount])

                    channel = await member.create_dm()
            
                    dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\n{amount} <:doughnut:831895771442839552> donut(s)', color=0x00ff00)
                    await channel.send(embed=dm_embed)

                    await ctx.send(f'You gave **{member}** {amount} donut(s) <:doughnut:831895771442839552>')

        dbase.commit()
        dbase.close()

    '''
    Money Making
    '''
    #Beg
    @commands.command()
    @commands.cooldown(1, 35, commands.BucketType.user)
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
            'Karal',
            'James Charls',
            'Jeff Bezos',
            'Crunchymeatguy',
            'Darkside',
            'London',
            'Dank Mazen',
            'Bruni',
            'Wiggle The Great',
            'The Orange Fresh',
            'Skeppy',
            'Copi',
            'Papercat',
            'Ethereal',
            'DUKEØFDØØM'
        ]

        amount = random.randint(100, 1000)

        cursor.execute(f"SELECT doughnut FROM multis WHERE user_id = '{ctx.author.id}'")
        doughnut_amount = cursor.fetchone()
        doughnut_amount = (doughnut_amount[0])

        if doughnut_amount > 0:
            if doughnut_amount > 5:
                max = 5
                new_amount = amount * (1 + (0.05 * max))
                new_amount = int(new_amount)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, new_amount, new_amount])

                amount = ('{:,}'.format(amount))
                await ctx.reply(f'{random.choice(names)} gave you <:dankmerchants:829809749058650152> **{amount}**!\n\nBut you happened to have at least <:doughnut:831895771442839552> 5 donut(s) on you that got you to <:dankmerchants:829809749058650152> **{int(new_amount)}**')
            
            else:
                new_amount = amount * (1 + (0.05 * doughnut_amount))
                new_amount = int(new_amount)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, new_amount, new_amount])

                amount = ('{:,}'.format(amount))
                await ctx.reply(f'{random.choice(names)} gave you <:dankmerchants:829809749058650152> **{amount}**!\n\nBut you happened to have <:doughnut:831895771442839552> **{doughnut_amount}** donut(s) on you that got you to <:dankmerchants:829809749058650152> **{int(new_amount)}**')

        else:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

            amount = ('{:,}'.format(amount))
            await ctx.reply(f'{random.choice(names)} gave you <:dankmerchants:829809749058650152> **{amount}**!')

        dbase.commit()
        dbase.close()

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Bet
    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bet(self, ctx, bet: int=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

        winner = [
            'yes',
            'no'
        ]

        cursor.execute(f"SELECT doughnut FROM multis WHERE user_id = '{ctx.author.id}'")
        doughnut_result = cursor.fetchone()
        doughnut_result = (doughnut_result[0])

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        result = (result[0])

        if bet == None:
            await ctx.reply('You actully have to bet something dumb dumb (0)_(0)')

        else:
            if bet < 0:
                await ctx.send('Dont even try me')

            else:

                if bet < 100:
                    await ctx.reply('You have to bet at least 100')

                else:

                    if result < bet:
                        await ctx.reply('You dont have enough money to do that!')

                    else:

                        if bet <= 500000:
                            new_bet = bet * 2
                            amount = random.randint(bet, new_bet)
                            
                            win = random.choice(winner)

                            if win == 'yes':
                                if doughnut_result > 0:
                                    if doughnut_result > 5:

                                        max = 5
                                        new_amount = amount * (1 + (0.05 * max))
                                        new_amount = int(new_amount)

                                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, new_amount, new_amount])

                                        embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                                        embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{amount}`\n\nBut you had at least <:doughnut:831895771442839552> 5 donuts with you so that got you to <:dankmerchants:829809749058650152>** {int(new_amount)}**')
                                        await ctx.reply(embed=embed)

                                    else:

                                        new_amount = amount * (1 + (0.05 * doughnut_result))
                                        new_amount = int(new_amount)

                                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, new_amount, new_amount])

                                        embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                                        embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{amount}`\n\nBut you had <:doughnut:831895771442839552> **{doughnut_result}** donut(s) with you so that got you to <:dankmerchants:829809749058650152>** {int(new_amount)}**')
                                        await ctx.reply(embed=embed)

                                else:
                                    cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

                                    embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                                    embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{amount}`')
                                    await ctx.reply(embed=embed)

                            if win == 'no':

                                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, bet, bet])

                                embed = discord.Embed(title='Bet Results', description='You lost', color=0xff0000)
                                embed.add_field(name='You lost:', value=f'<:dankmerchants:829809749058650152> `{bet}`')
                                await ctx.reply(embed=embed)

                        if bet > 500000:
                            await ctx.reply('Woah there the max you can bet is 500k at a time!')

        dbase.commit()
        dbase.close()

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'If I let you go now you wouldnt have much money\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Work
    @commands.command()
    async def work(self, ctx):
        client = self.client

        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        await ctx.reply('What would you like to do to work?\n`Mine`\n`Chop`\n`Hunt`\n`Fish`')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for('message', check=check)

        #Mine
        if msg.clean_content.lower() == 'mine':
            yes_no = [
                'yes',
                'no'
            ]

            fight = random.choice(yes_no)

            if fight == 'yes':
                await ctx.send(f'You went mining but there was a bit of a suprise waiting for you... QUICK what do you want to do?\nLeave the mine as fast as you can and leave you loot **or** fight and be able to get some extra loot! What would you like to do?\n**Fight** *or* **Run**')
                
                msg = await client.wait_for('message', check=check)

                if msg.clean_content.lower() == 'fight':
                    win = random.choice(yes_no)

                    if win == 'yes':
                        await ctx.send('You killed the monster and got away with some stuff\ncoming soon...')

                    if win == 'no':
                        await ctx.send('Well... you died so you got nothing')

                if msg.clean_content.lower() == 'run':
                    win = random.choice(yes_no)

                    if win == 'yes':
                        await ctx.send('The monster left you alone so you ended up getting...')

                    if win == 'no':
                        await ctx.send('Well the monster got you and you died and got nothing')

            if fight == 'no':
                await ctx.send(f'You went mining and there were no monsters so you got out with stuff')

        #Chop
        if msg.clean_content.lower() == 'chop':
            pass

        #Hunt
        if msg.clean_content.lower() == 'hunt':
            await ctx.send('You went hunting')

        #Fish
        if msg.clean_content.lower() == 'fish':
            await ctx.send('You went fishing!')


        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Economy(client))