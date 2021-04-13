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
        await ctx.send('Coming Soon...')

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
        #Ducc
        if item == 'ducc' or item == 'duck':
            embed = discord.Embed(title='Duck', description='Its a duck that happens to be pretty powerful and annoying...', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/784491141022220312/830801553714577468/ducc.png')
            embed.add_field(name='Price:', value='Item Not Purchasable')
            await ctx.send(embed=embed)
        #Reaction
        if item == 'reaction':
            embed = discord.Embed(title='1 Week Auto Reaction', description='When your name is pinged make the bot auto react', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **75,000**')
            await ctx.send(embed=embed)

        #Premium
        if item == 'premium':
            embed = discord.Embed(title='1 Premium', description='Get special server perks', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/797290098189664256.gif?v=1')
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)

        #Giveaway Bypass
        if item == 'bypass':
            embed = discord.Embed(title='1 Week Giveaway Bypass', description='Bypass all giveaways', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)
        
        #Custom Channel
        if item == 'channel':
            embed = discord.Embed(title='1 Week Custom Channel', description='Get a custom channel that only you can access', color=0x00ff00)
            embed.add_field(name='Price:', value='<:dankmerchants:829809749058650152> **250,000**')
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
            if bal >= 100000:
                role = discord.utils.find(lambda r: r.name == '👑 Premium', ctx.message.guild.roles)
                if role in member.roles:
                    await ctx.send('You already have premium active!')

                else:
                    amount = 100000
                    cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                    role = discord.utils.get(ctx.guild.roles, name='👑 Premium')
                    await member.add_roles(role)
                    await ctx.send('Enjoy your premium!')
            else:
                await ctx.send('You dont have enough money to buy that!')

        #Auto Reaction
        if item == 'reaction':
            if bal >= 75000:
                amount = 75000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                await ctx.send('Puchase complete! Please go ask a mod to get your auto reaction set up and make sure to show them this confirmation message as well')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Giveaway Bypass
        if item == 'bypass':
            if bal >= 100000:
                amount = 100000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                role = discord.utils.get(ctx.guild.roles, name='bypass access')
                await member.add_roles(role)
                await ctx.send('Enjoy your giveaway bypasses!')

            else:
                await ctx.send('You dont have enough money to buy that!')

        #Channel
        if item == 'channel':
            if bal >= 250000:
                amount = 250000
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])

                await ctx.send('Puchase complete! Please go ask a mod to get your auto reaction set up and make sure to show them this confirmation message as well')

            else:
                await ctx.send('You dont have enough money to buy that!')

        '''
        BOXES
        '''
        #Wooden Box
        if item == 'wooden':
            if bal >= 50000:
                amount = 50000
                box = 1
                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO economy (user_id, woodenbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodenbox = woodenbox + ?;", [user, box, box])

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
        if item == 'wooden':
            cursor.execute(f"SELECT woodenbox FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1

                cursor.execute("INSERT INTO economy (user_id, woodenbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodenbox = woodenbox - ?;", [user, box, box])
                
                coins = random.randint(1000, 50000)
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

                coins = random.randint(10000, 100000)
                appleamount = random.randint(0, 10)
                duckamount = random.randint(1, 5)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [duck, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n**Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

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

                coins = random.randint(10000, 250000)
                appleamount = random.randint(0, 15)
                duckamount = random.randint(1, 10)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [duck, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n**Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

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

                coins = random.randint(25000, 500000)
                appleamount = random.randint(1, 25)
                duckamount = random.randint(1, 25)
                goldenamount = random.randint(0, 3)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])
                cursor.execute("INSERT INTO economy (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox + ?;", [user, goldenamount, goldenamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`\n***Gold Boxes:*** `{goldenamount}`')

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

                coins = random.randint(25000, 1000000)
                appleamount = random.randint(1, 50)
                duckamount = random.randint(1, 10)
                donutamount = random.randint(0, 1)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO economy (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO economy (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])
                cursor.execute("INSERT INTO economy (user_id, donut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET donut = donut + ?;", [user, donutamount, donutamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`\n***Donuts:*** `{donutamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        dbase.commit()
        dbase.close()

    '''
    Money Making
    ''' 
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
            'Darkside'
        ]

        amount = random.randint(50, 1000)

        cursor.execute(f"SELECT donut FROM economy WHERE user_id = '{ctx.author.id}'")

        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

        amount = ('{:,}'.format(amount))
        await ctx.send(f'{random.choice(names)} Gave you <:dankmerchants:829809749058650152> **{amount}**!')

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

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        result = (result[0])

        if bet == None:
            await ctx.send('You actully have to bet something dumb dumb (0)_(0)')

        else:

            if result < bet:
                await ctx.send('You dont have enough money to do that!')

            else:

                if bet <= 500000:
                    amount = random.randint(0, bet)
                    
                    win = random.choice(winner)

                    if win == 'yes':
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

                        embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                        embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{amount}`')
                        await ctx.send(embed=embed)

                    if win == 'no':

                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, bet, bet])

                        embed = discord.Embed(title='Bet Results', description='You lost', color=0xff0000)
                        embed.add_field(name='You lost:', value=f'<:dankmerchants:829809749058650152> `{bet}`')
                        await ctx.send(embed=embed)

                if bet > 500000:
                    await ctx.send('Woah there the max you can bet is 500k at a time!')

        dbase.commit()
        dbase.close()

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'If I let you go now you wouldnt have much money\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))