import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import sqlite3

import random

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def on_message(self, message):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        user = message.author.id

        if result is None:
            balance = 0

            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance = ?;", [user, balance, balance])

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
                cursor.execute(f"SELECT woodbox FROM economy WHERE user_id = '{ctx.author.id}'")
                woodbox = cursor.fetchone()
                woodbox = (woodbox[0])

                cursor.execute(f"SELECT ironbox FROM economy WHERE user_id = '{ctx.author.id}'")
                ironbox = cursor.fetchone()
                ironbox = (ironbox[0])

                cursor.execute(f"SELECT goldbox FROM economy WHERE user_id = '{ctx.author.id}'")
                goldbox = cursor.fetchone()
                goldbox = (goldbox[0])

                cursor.execute(f"SELECT diamondbox FROM economy WHERE user_id = '{ctx.author.id}'")
                diamondbox = cursor.fetchone()
                diamondbox = (diamondbox[0])

                cursor.execute(f"SELECT emeraldbox FROM economy WHERE user_id = '{ctx.author.id}'")
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
                cursor.execute(f"SELECT doughnut FROM economy WHERE user_id = '{ctx.author.id}'")
                doughnut = cursor.fetchone()
                doughnut = (doughnut[0])

                embed = discord.Embed(title=f'{ctx.author}s Inventory', description='Multipliers', color=0x00ff00)
                embed.add_field(name=f'<:doughnut:831895771442839552> __Doughnut 5%__', value=f'**{doughnut}** owned', inline=False)
                embed.set_footer(text='Page 2-2')
                await ctx.send(embed=embed)

        else:
            
            if page == '1' or page == None:
                cursor.execute(f"SELECT woodbox FROM economy WHERE user_id = '{member.id}'")
                woodbox = cursor.fetchone()
                woodbox = (woodbox[0])

                cursor.execute(f"SELECT ironbox FROM economy WHERE user_id = '{member.id}'")
                ironbox = cursor.fetchone()
                ironbox = (ironbox[0])

                cursor.execute(f"SELECT goldbox FROM economy WHERE user_id = '{member.id}'")
                goldbox = cursor.fetchone()
                goldbox = (goldbox[0])

                cursor.execute(f"SELECT diamondbox FROM economy WHERE user_id = '{member.id}'")
                diamondbox = cursor.fetchone()
                diamondbox = (diamondbox[0])

                cursor.execute(f"SELECT emeraldbox FROM economy WHERE user_id = '{member.id}'")
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
                cursor.execute(f"SELECT doughnut FROM economy WHERE user_id = '{member.id}'")
                doughnut = cursor.fetchone()
                doughnut = (doughnut[0])

                embed = discord.Embed(title=f'{member}s Inventory', description='Multipliers', color=0x00ff00)
                embed.add_field(name=f'<:doughnut:831895771442839552> __Doughnut 5%__', value=f'**{doughnut}** owned', inline=False)
                embed.set_footer(text='Page 2-2')
                await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    #Shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx, item=None):
        #Page 1
        if item is None or item == '1':
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<a:omega:791410419624443934> **1 Week Auto Reaction** - <:dankmerchants:829809749058650152> 700,000\n\n<a:premium:797290098189664256> **1 Week Server Premium** - <:dankmerchants:829809749058650152> 700,000\n\n<a:bypass:829822077795958785> **1 Week Giveaway Bypass** - <:dankmerchants:829809749058650152> 1,000,000\n\n🏡 **1 Week Custom Channel** - <:dankmerchants:829809749058650152> 1,000,000\n\n<a:blob:829822719372951592> **1 Week Custom Role** - <:dankmerchants:829809749058650152> 650,000', color=0x00ff00)
            embed.set_footer(text='Page 1-2')
            await ctx.send(embed=embed)

        #Page 2
        if item == '2':
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<:woodbox:830211928595890206> **Wood Loot Box** - <:dankmerchants:829809749058650152> 50,000\n\n<:ironbox:830197241934512188> **Iron Loot Box** - <:dankmerchants:829809749058650152> 100,000\n\n<:goldbox:830197220405805147> **Gold Loot Box** - <:dankmerchants:829809749058650152> 250,000\n\n<:diamondbox:830197220007477259> **Diamond Loot Box** - <:dankmerchants:829809749058650152> 500,000\n\n<:emeraldbox:830216613755486229> **Emerald Loot Box** - <:dankmerchants:829809749058650152> 1,000,000', color=0x00ff00)
            embed.set_footer(text='Page 2-2')
            await ctx.send(embed=embed)
        #Ducc
        if item == 'ducc' or item == 'duck':
            embed = discord.Embed(title='Duck', description='Its a duck that happens to be pretty powerful and annoying...', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/784491141022220312/830801553714577468/ducc.png')
            embed.add_field(name='Price:', value='Item Not Purchasable')
            await ctx.send(embed=embed)
        #Donut
        if item == 'doughnut' or item == 'donut':
            embed = discord.Embed(title='Dount', description='A dount that happens to give you a 5% multi cap of 25%', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/831895771442839552.png?v=1')
            embed.add_field(name='Price:', value='Item Not Purchasable')
            await ctx.send(embed=embed)
        #Reaction
        if item == 'reaction':
            embed = discord.Embed(title='1 Week Auto Reaction', description='When your name is pinged make the bot auto react', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **700,000**')
            await ctx.send(embed=embed)
        #Premium
        if item == 'premium':
            embed = discord.Embed(title='1 Premium', description='Get special server perks', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/797290098189664256.gif?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **750,000**')
            await ctx.send(embed=embed)

        #Giveaway Bypass
        if item == 'bypass':
            embed = discord.Embed(title='1 Week Giveaway Bypass', description='Bypass all giveaways', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **1,000,000**')
            await ctx.send(embed=embed)
        
        #Custom Channel
        if item == 'channel':
            embed = discord.Embed(title='1 Week Custom Channel', description='Get a custom channel that only you can access', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **1,000,000**')
            await ctx.send(embed=embed)

        #Custom Role
        if item == 'role':
            embed = discord.Embed(title='1 Week Custom Role', description='Get a custom Role that only you can access', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **650,000**')
            await ctx.send(embed=embed)

        #Wooden Box
        if item == 'wood' or item == 'wooden':
            embed = discord.Embed(title='Wooden Box', description='A basic wooden box that could find you some loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830211928595890206.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **50,000**')
            await ctx.send(embed=embed)

        #Iron Box
        if item == 'iron':
            embed = discord.Embed(title='Iron Box', description='A solid iron box probally has some good stuff in it', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197241934512188.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)

        #Gold Box
        if item == 'gold':
            embed = discord.Embed(title='Gold Box', description='A solid gold box that must have good loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220405805147.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **250,000**')
            await ctx.send(embed=embed)

        #Diamond Box
        if item == 'diamond':
            embed = discord.Embed(title='Diamond Box', description='A solid diamond box that is bound to have good loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220007477259.png?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **500,000**')
            await ctx.send(embed=embed)

        #Emerald Box
        if item == 'emerald':
            embed = discord.Embed(title='Emerald Box', description='The best box of them all that will have the best loot', color=0x00ff00)
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

        member = ctx.author
        user = ctx.author.id

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        bal = (result[0])

        if item == None:
            await ctx.send('You actully have to name a item to buy it (0)_(0)')
        '''
        OTHER
        '''
        if item == 'ducc' or item == 'duck':
            await ctx.send('This item can not be bought')

        '''
        PERKS
        '''
        #Premium
        if item == 'premium':
            if bal >= 750000:
                role = discord.utils.find(lambda r: r.name == '👑 Premium', ctx.message.guild.roles)
                if role in member.roles:
                    await ctx.send('You already have premium active!')

                else:
                    amount = 750000
                    cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                    role = discord.utils.get(ctx.guild.roles, name='👑 Premium')
                    await member.add_roles(role)
                    await client.get_channel(787761394664996865).send(f'{ctx.author} bought 1 week premium that needs to be removed in 1 week')
                    await ctx.send('Enjoy your premium!')
            else:
                await ctx.send('You dont have enough money to buy that!')

        #Auto Reaction
        if item == 'reaction':
            if bal >= 700000:
                amount = 700000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                await ctx.send('Puchase complete! Please go ask a mod to get your auto reaction set up and make sure to show them this confirmation message as well')
                await client.get_channel(787761394664996865).send(f'{ctx.author} bought 1 week auto reaction that needs to be set up please help them')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Giveaway Bypass
        if item == 'bypass':
            if bal >= 1000000:
                amount = 1000000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                role = discord.utils.get(ctx.guild.roles, name='bypass access')
                await member.add_roles(role)
                await ctx.send('Enjoy your giveaway bypasses!')
                await client.get_channel(787761394664996865).send(f'{ctx.author} bought 1 giveaway bypass that needs to be removed in 1 week')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Channel
        if item == 'channel':
            if bal >= 1000000:
                amount = 1000000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                await ctx.send('Puchase complete! Please go ask a mod to get your auto reaction set up and make sure to show them this confirmation message as well')
                await client.get_channel(787761394664996865).send(f'{ctx.author} bought 1 week custom channel please help them set it up')

            else:
                await ctx.send('You dont have enough money to buy that!')

        '''
        BOXES
        '''
        #Wooden Box
        if item == 'wooden' or item == 'wood':
            if bal >= 50000:
                amount = 50000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO economy (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [user, box, box])

                await ctx.send('Enjoy your wooden box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Iron Box
        if item == 'iron':
            if bal >= 100000:
                amount = 100000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO economy (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox + ?;", [user, box, box])

                await ctx.send('Enjoy your iron box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Gold Box
        if item == 'gold':
            if bal >= 250000:
                amount = 250000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO economy (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox + ?;", [user, box, box])

                await ctx.send('Enjoy your gold box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Diamond Box
        if item == 'diamond':
            if bal >= 500000:
                amount = 500000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO economy (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox + ?;", [user, box, box])

                await ctx.send('Enjoy your diamond box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Emerald Box
        if item == 'emerald':
            if bal >= 1000000:
                    amount = 1000000
                    box = 1
                    cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO economy (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox + ?;", [user, box, box])

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
            cursor.execute(f"SELECT woodbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1

                cursor.execute("INSERT INTO economy (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox - ?;", [user, box, box])
                
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
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Gold Box
        if item == 'gold':
            cursor.execute(f"SELECT goldbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO economy (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox - ?;", [user, box, box])

                coins = random.randint(100000, 250000)
                appleamount = random.randint(0, 15)
                duckamount = random.randint(1, 10)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

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
                cursor.execute("INSERT INTO economy (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox - ?;", [user, box, box])

                coins = random.randint(250000, 500000)
                appleamount = random.randint(1, 25)
                duckamount = random.randint(1, 25)
                donutamount = random.randint(0, 1)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

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
                cursor.execute("INSERT INTO economy (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox - ?;", [user, box, box])

                coins = random.randint(500000, 1000000)
                appleamount = random.randint(1, 50)
                duckamount = random.randint(1, 10)
                donutamount = random.randint(0, 1)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])
                cursor.execute("INSERT INTO economy (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [user, donutamount, donutamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`\n***Donuts:*** `{donutamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        dbase.commit()
        dbase.close()

    '''
    Money Making
    '''
    #Daily
    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id
        coins = 25000000

        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])

        await ctx.send('Daily collected!\n<:dankmerchants:829809749058650152> **25,000**')

        dbase.commit()
        dbase.close()

    @daily.error
    async def daily_error(self, ctx, error):
        await ctx.send('This command isnt out yet!')

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

        cursor.execute(f"SELECT doughnut FROM economy WHERE user_id = '{ctx.author.id}'")
        doughnut_amount = cursor.fetchone()
        doughnut_amount = (doughnut_amount[0])

        if doughnut_amount > 0:
            if doughnut_amount > 5:
                max = 5
                new_amount = amount * (1 + (0.05 * max))
                new_amount = int(new_amount)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, new_amount, new_amount])

                amount = ('{:,}'.format(amount))
                await ctx.reply(f'{random.choice(names)} gave you <:dankmerchants:829809749058650152> **{amount}**!\n\nBut you happened to have <:doughnut:831895771442839552> **{doughnut_amount}** donut(s) on you that got you to <:dankmerchants:829809749058650152> **{int(new_amount)}** but only 5 donuts were used')
            
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
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bet(self, ctx, bet: int=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

        winner = [
            'yes',
            'no'
        ]

        cursor.execute(f"SELECT doughnut FROM economy WHERE user_id = '{ctx.author.id}'")
        doughnut_result = cursor.fetchone()
        doughnut_result = (doughnut_result[0])

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        result = (result[0])

        if bet == None:
            await ctx.reply('You actully have to bet something dumb dumb (0)_(0)')

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
                                    embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{amount}`\n\nBut you had <:doughnut:831895771442839552> **{doughnut_result}** donut(s) with you so that got you to <:dankmerchants:829809749058650152>** {int(new_amount)}** but only 5 donuts did the job')
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

    '''
    Giving
    '''

    #Give
    @commands.command()
    async def give(self, ctx, member: discord.Member, amount=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member == None:
            await ctx.reply('You actully have to give stuff to someone')

        else:
            user = ctx.author.id
            member_id = member.id

            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            await ctx.send(f'{ctx.author.mention} you gave **{member}** <:dankmerchants:829809749058650152> **{amount}**')

        dbase.commit()
        dbase.close()

    #Gift
    @commands.command()
    async def gift(self, ctx, amount=None, item=None, member: discord.Member=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        if member == None:
            await ctx.reply('You actully have to give stuff to someone')

        else:
            if item == 'wood' or item == 'wooden':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            if item == 'iron':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            if item == 'gold':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            if item == 'diamond':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            if item == 'emerald':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

            if item == 'donut' or item == 'doughnut' or item == 'dough':
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Economy(client))