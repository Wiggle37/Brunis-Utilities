import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import asyncio
import sqlite3
import random
from datetime import datetime

from discord.ext.commands.core import command
from items_bruni import doughnut, economy_items, currency
from itertools import islice
import traceback
import sys
import typing

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.items = economy_items
        self.currency = currency

    '''
    Functions
    '''
    #Number Converter
    def is_valid_int(self, amount):
        try:
            float(amount.replace("m","").replace("k",""))
            return int(eval(amount.replace("k","e3").replace("m", "e6")))
            
        except ValueError:
            return False
    
    def beautify_number(self, num):
        if num is None: return ""
        return '{:,}'.format(num)

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

        if result is None:
            user = message.author.id
            balance = 500

            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, balance, balance])

        cursor.execute(f"SELECT user_id FROM boxes WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [user, amount, amount])

        cursor.execute(f"SELECT user_id FROM multis WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [user, amount, amount])

        cursor.execute(f"SELECT user_id FROM items WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, amount, amount])

        cursor.execute(f"SELECT user_id FROM materials WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO materials (user_id, wood) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wood = wood + ?;", [user, amount, amount])

        cursor.execute(f"SELECT user_id FROM collectables WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO collectables (user_id, wiggle) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wiggle = wiggle + ?;", [user, amount, amount])

        cursor.execute(f"SELECT user_id FROM tools WHERE user_id = '{message.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = message.author.id
            amount = 0

            cursor.execute("INSERT INTO tools (user_id, woodpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodpick = woodpick + ?;", [user, amount, amount])

        dbase.commit()
        dbase.close()

    '''
    General
    '''
    #Balance
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member = None):        
        user = member or ctx.author
        
        amount = self.currency.get_amount(user.id)
        bal_embed = discord.Embed(
            title = f"{user.name}'s balance",
            description = f"**Balance:**\n{self.currency.emoji} {self.beautify_number(amount)}",
            colour = 0x00ff00
        )
        await ctx.send(embed = bal_embed)
    
    @balance.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("That isn't a valid user")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        
    #Rich
    @commands.command()
    async def rich(self, ctx):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()

        cursor.execute("SELECT balance, user_id FROM economy ORDER BY balance DESC")
        richest = cursor.fetchmany(10)

        rich_embed = discord.Embed(title="Richest People In Dank Merchants", colour=0x00ff00)

        embed_desc = ""
        dank_merchants = self.client.get_guild(784491141022220309)
        for rank, user_info in enumerate(richest):
            member = dank_merchants.get_member(int(user_info[1]))
            embed_desc += f"**{rank + 1}. {member}:** <:dankmerchants:829809749058650152> `{'{:,}'.format(user_info[0])}`\n"

        rich_embed.description = embed_desc
        await ctx.send(embed = rich_embed)

        dbase.close()

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, member: typing.Optional[discord.Member] = None, page: typing.Optional[int] = 1):
        item_limit_per_page = 5 # for displaying a maximum number of items in the inventory

        user = member or ctx.author

        inv_embed = discord.Embed(
            title = f"{user.name}’s Inventory" ,
            colour = 0x00ff00
        )

        user_items = self.items.copy() # will be left with items that the user has
        for name, item in self.items.copy().items():
            quantity = item.get_item_count(user.id)
            if quantity == 0:
                del user_items[name]
            else:
                user_items[name] = quantity
        
        if user_items == {}:
            return await ctx.send("You don't have any items!")

        for name, item_count in dict(islice(user_items.items(), (page - 1) * 5, page *5)).items():
            inv_embed.add_field(
                name = f"{self.items[name].emoji} __{self.items[name].name}__",
                value = f"**{self.beautify_number(item_count)}** owned",
                inline = False
            )
            
        if inv_embed.fields == []:            
            return await ctx.send(f"Page {page} doesn’t exist")
        
        total_pages = len(user_items) // item_limit_per_page + 1
        inv_embed.set_footer(text = f"Page {page} of {total_pages}")
        return await ctx.send(embed = inv_embed)

    #Shop
    @commands.command(aliases = ["store"])
    async def shop(self, ctx, page: typing.Optional[int], *, item_name = None):
        if page is None and item_name is None:
            return await self.shop(ctx, 1)

        is_item = False
        if page is None and item_name is not None:
            is_item = True
        
        if page is not None and page <= 0:
            return await ctx.send("You need to key in a valid page")

        for name, item in self.items.items():
            if not is_item:
                break

            if item_name.lower().replace(" ", "") not in name.lower().replace(" ", ""):
                continue

            item_info_embed = discord.Embed(
                title = f"{item.name} ({self.beautify_number(item.get_item_count(ctx.author.id))} owned)",
                description = item.description,
                colour = 0x00ff00
            )
            
            item_info_embed.add_field(
                name = "Buy: ",
                value = item.purchasable * f"{self.currency.emoji} **{self.beautify_number(item.price)}**" + (not item.purchasable) * "This item cannot be bought",
                inline = False
            )

            item_info_embed.add_field(
                name = "Sell: ",
                value = item.sellable * f"{self.currency.emoji} **{self.beautify_number(item.sell_price)}**" + (not item.sellable) * "This item cannot be sold",
                inline = False
            )

            item_info_embed.set_thumbnail(url = item.image_url)
            return await ctx.send(embed = item_info_embed)
        
        if is_item:
            return await ctx.send("That's not a valid item")
        
        purchasable_items = [item for item in self.items.values() if item.purchasable]

        item_limit_per_page = 5
        pages_of_shop = len(purchasable_items) // item_limit_per_page + 1

        if page > pages_of_shop:
            return await ctx.send("That's not a valid page number")

        shop_embed = discord.Embed(
            title = "Dank Merchants Shop",
            description = "__**Shop Items:**__\n\n",
            colour = 0x00ff00
        )

        for item in purchasable_items[(page - 1) * item_limit_per_page: page * item_limit_per_page]:
            shop_embed.description += f"{item.emoji} **{item.name}** - {self.currency.emoji} {self.beautify_number(item.price)}\n\n"
        shop_embed.set_footer(text = f"Page {page} of {pages_of_shop}")

        return await ctx.send(embed = shop_embed)
    #Buy
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, count: int, *, item_name):
        if count <= 0:
            return await ctx.send("You need to key in an valid amount, dummy")       

        purchasable_items = [name for name, item_class in self.items.items() if item_class.purchasable]

        for name in purchasable_items:
            if item_name.lower().replace(" ", "") not in name.lower().replace(" ", ""):
                continue

            if self.currency.get_amount(ctx.author.id) < self.items[name].price * count:
                return await ctx.send("You don't have enough money for that LMAO")

            self.items[name].purchase_items(ctx.author.id, count)
            return await ctx.send(f"Bought {count} {name}, paid {self.currency.emoji} {self.beautify_number(self.items[name].price * count)}")
        
        return await ctx.send("That wasn't a valid item to buy")

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("It's `b!buy <amount> <item>`")
        
        if isinstance(error, commands.errors.BadArgument):
            return await ctx.send("You need to key in an amount of items to buy")

        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
       
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, count: int, *, item_name):
        if count <= 0:
            return await ctx.send("You need to key in an valid amount, dummy")       

        sellable_items = [name for name, item_class in self.items.items() if item_class.sellable]

        for name in sellable_items:
            if item_name.lower().replace(" ", "") not in name.lower().replace(" ", ""):
                continue

            if self.items[name].get_item_count(ctx.author.id) < count:
                return await ctx.send("You literally don't have that many items smh")

            self.items[name].sell_items(ctx.author.id, count)
            return await ctx.send(f"Sold {count} {name}, got {self.currency.emoji} {self.beautify_number(self.items[name].sell_price * count)}")
        
        return await ctx.send("That wasn't a valid item to sell")

    @sell.error
    async def sell_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("It's `b!sell <amount> <item>`")
        
        if isinstance(error, commands.errors.BadArgument):
            return await ctx.send("You need to key in an amount of items to sell")

        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    
    #Use
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx,  count: typing.Optional[int] = 1, *, item_name):
        if count <= 0:
            return await ctx.send("You can’t use that number of items, dummy")

        for name, item_class in self.items.items():
            if item_name.lower().replace(" ", "") not in name.lower().replace(" ", ""):
                continue

            if item_class.table != "boxes": # the only items that can be used thus far
                return await ctx.send("That item cannot be used!")

            if item_class.get_item_count(ctx.author.id) < count:
                return await ctx.send("You literally don't have that enough items to use")
            
            response = item_class.usage(ctx.author.id, count) 

            return await ctx.send(response)

        return await ctx.send("That's not a valid item")
    

    @use.error
    async def use_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)

        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("It's `b!use (amount) <item>`")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    '''
    Giving
    '''
    #Give
    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('That isnt a valid number')

        else:
            cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()

            if result[0] < amount:
                await ctx.send('You dont have enough money to do that')

            else:
                if member == None:
                    await ctx.reply('You actully have to give stuff to someone')

                else:
                    if amount < 0:
                        await ctx.send('Dont even try me dumbass')

                    else:
                        user = ctx.author.id
                        member_id = member.id

                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [member_id, amount, amount])
                        
                        await ctx.send(f'{ctx.author.mention} you gave **{member}** <:dankmerchants:829809749058650152> **{amount}**')

                        channel = await member.create_dm()
                    
                        dm_embed = discord.Embed(title=f'You have a gift!', description=f'You have a gift from {ctx.message.author}\nYou got <:dankmerchants:829809749058650152> **{amount}** from {ctx.message.author}', color=0x00ff00)
                        await channel.send(embed=dm_embed)

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
                    cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut - ?;", [user, amount, amount])
                    cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [member_id, amount, amount])

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
        doughnut_amount = doughnut.get_item_count(ctx.author.id)
        amount = random.randint(100, 1000)

        names = [
            'Lily',
            'Darkside',
            'Dark',
            'Neon',
            'London',
            'Dank Mazen',
            'Bruni',
            'Wiggle',
            'The Orange Fresh',
            'Skeppy',
            'Copi',
            'Papercat',
            'Ethereal',
            'DUKEØFDØØM',
            'Adit',
            'Tommy',
            'Julesi'
        ]

        if doughnut_amount <= 0:
            self.currency.add(ctx.author.id, int(amount))

            await ctx.send(f'**{random.choice(names)}** gave you <:dankmerchants:829809749058650152> {int(amount)}')

        if doughnut_amount > 0 and doughnut_amount < 5:
            new_amount = int(amount * (1 + 0.05 * doughnut_amount))
            self.currency.add(ctx.author.id, int(new_amount))

            await ctx.send(f'**{random.choice(names)}** gave you <:dankmerchants:829809749058650152> {int(amount)} but you had <:doughnut:831895771442839552> {doughnut_amount} with you that ended up giveing you a total of {int(new_amount)}')

        if doughnut_amount > 5:
            new_amount = int(amount * (1 + (0.05 * 5)))
            self.currency.add(ctx.author.id, int(new_amount))

            await ctx.send(f'**{random.choice(names)}** gave you <:dankmerchants:829809749058650152> {amount}')

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Bet
    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bet(self, ctx, bet: str=None):
        bet = self.is_valid_int(bet)
        if bet == False:
            await ctx.send('That is not a valid number')

        else:
            if bet > 500000:
                await ctx.send('That max you can bet is 500k at a time')

            else:
                bal = self.currency.get_amount(ctx.author.id)

                if bal < bet:
                    await ctx.send('You dont have enough money to do that')

                else:
                    win = random.choice(['yes', 'no'])

                    if win == 'yes':
                        amount = bet * 1.5

                        dougnut_amount = doughnut.get_item_count(ctx.author.id)
                        if dougnut_amount > 0 and dougnut_amount < 5:
                            new_amount = int(amount * (1 + (0.05 * dougnut_amount)))

                            self.currency.add(ctx.author.id, new_amount)

                            embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                            embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{int(amount)}`\n\nYou had <:doughnut:831895771442839552> {dougnut_amount} doughnuts that gave you a multi and you ended up getting: <:dankmerchants:829809749058650152>** {int(new_amount)}**')
                            await ctx.reply(embed=embed)


                        if dougnut_amount >= 5:
                            new_amount = int(amount * (1 + (0.05 * 5)))

                            self.currency.add(ctx.author.id, new_amount)

                            embed = discord.Embed(title='Bet Results', description='You Won', color=0x00ff00)
                            embed.add_field(name='Your payout was:', value=f'<:dankmerchants:829809749058650152> `{int(amount)}`\n\nBut you had at least <:doughnut:831895771442839552> 5 donuts with you so that got you to <:dankmerchants:829809749058650152>** {int(new_amount)}**')
                            await ctx.reply(embed=embed)


                    else:
                        self.currency.subtract(ctx.author.id, bet)

                        embed = discord.Embed(title='Bet Results', description='You lost, sucks', color=0xff0000)
                        embed.add_field(name='You lost:', value=f'<:dankmerchants:829809749058650152> `{bet}`')
                        await ctx.reply(embed=embed)

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'If I let you go now you wouldnt have much money\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Work
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def work(self, ctx):
        client = self.client

        user = ctx.author.id

        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        yes_no = [
                'yes',
                'no'
            ]

        await ctx.reply('What would you like to do to work?\n`Mine`\n`Chop`\n`Hunt`\n`Fish`')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for('message', check=check, timeout=15)

        try:
            #Mine
            if msg.clean_content.lower() == 'mine':
                cursor.execute(f"SELECT woodpick FROM tools WHERE user_id = '{ctx.author.id}'")
                woodpick = cursor.fetchone()
                woodpick = (woodpick[0])

                if woodpick < 1:
                    await ctx.send('Umm You need at least a wood pickaxe to go mining do `b!buy woodpick`')

                else:
                    cursor.execute(f"SELECT ironpick FROM tools WHERE user_id = '{ctx.author.id}'")
                    ironpick = cursor.fetchone()
                    ironpick = (ironpick[0])

                    if ironpick < 1:
                        iron = random.randint(1, 1)

                        cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron + ?;", [user, iron, iron])

                        await ctx.send(f'You had an wood pick on you and got some loot\n`{iron}` iron')

                    else:
                        cursor.execute(f"SELECT goldpick FROM tools WHERE user_id = '{ctx.author.id}'")
                        goldpick = cursor.fetchone()
                        goldpick = (goldpick[0])

                        if goldpick < 1:
                            iron = random.randint(1, 3)

                            cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron + ?;", [user, iron, iron])

                            await ctx.send(f'You had an iron pick on you and got some loot\n`{iron}` iron')

                        else:
                            cursor.execute(f"SELECT diamondpick FROM tools WHERE user_id = '{ctx.author.id}'")
                            diamondpick = cursor.fetchone()
                            diamondpick = (diamondpick[0])

                            if diamondpick < 1:
                                gold = random.randint(1, 3)
                                iron = random.randint(1, 5)

                                cursor.execute("INSERT INTO materials (user_id, gold) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gold = gold + ?;", [user, gold, gold])
                                cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron + ?;", [user, iron, iron])

                                await ctx.send(f'You had an gold pick on you and got some loot\n`{gold}` gold\n`{iron}` iron')

                            else:
                                cursor.execute(f"SELECT emeraldpick FROM tools WHERE user_id = '{ctx.author.id}'")
                                emeraldpick = cursor.fetchone()
                                emeraldpick = (emeraldpick[0])

                                if emeraldpick < 1:
                                    diamond = random.randint(1, 7)
                                    gold = random.randint(3, 5)
                                    iron = random.randint(3, 7)

                                    cursor.execute("INSERT INTO materials (user_id, diamond) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamond = diamond + ?;", [user, diamond, diamond])
                                    cursor.execute("INSERT INTO materials (user_id, gold) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gold = gold + ?;", [user, gold, gold])
                                    cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron + ?;", [user, iron, iron])

                                    await ctx.send(f'You had an diamond pick on you and got some loot\n`{diamond}` diamond\n`{gold}` gold\n`{iron}` iron')

                                else:
                                    emerald = random.randint(1, 3)
                                    diamond = random.randint(1, 15)
                                    gold = random.randint(3, 20)
                                    iron = random.randint(5, 15)

                                    cursor.execute("INSERT INTO materials (user_id, emerald) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emerald = emerald + ?;", [user, emerald, emerald])
                                    cursor.execute("INSERT INTO materials (user_id, diamond) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamond = diamond + ?;", [user, diamond, diamond])
                                    cursor.execute("INSERT INTO materials (user_id, gold) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gold = gold + ?;", [user, gold, gold])
                                    cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron + ?;", [user, iron, iron])

                                    await ctx.send(f'You had an EMERALD pick on you and got some loot\n`{emerald}` emerald\n`{diamond}` diamond\n`{gold}` gold\n`{iron}` iron')
                    
            #Chop
            if msg.clean_content.lower() == 'chop':
                amount = random.randint(1, 10)

                cursor.execute("INSERT INTO materials (user_id, wood) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wood = wood + ?;", [user, amount, amount])

                await ctx.send(f'You went to go chop down some trees and ended up getting <:mwood:835262637851541555> **{amount}** wood')

            #Hunt
            if msg.clean_content.lower() == 'hunt':
                cursor.execute(f"SELECT gun FROM tools WHERE user_id = '{ctx.author.id}'")
                result = cursor.fetchone()
                result = (result[0])

                if result < 1:
                    await ctx.send('You have to buy a gun first')

                else:
                    animals = [
                        'duck',
                        'goose',
                        'chicken'
                    ]
                    animal = random.choice(animals)
                    amount = 1

                    cursor.execute(f"INSERT INTO items (user_id, '{animal}') VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET '{animal}' = '{animal}' + ?;", [user, amount, amount])

                    if animal == 'duck':
                        await ctx.send(f'You went hunting and came back with a **duck**')

                    if animal == 'goose':
                        await ctx.send(f'You went hunting and came back with a **goose**')

                    if animal == 'chicken':
                        await ctx.send(f'You went hunting and came back with a **chicken**')

            #Fish
            if msg.clean_content.lower() == 'fish':
                cursor.execute(f"SELECT gun FROM tools WHERE user_id = '{ctx.author.id}'")
                result = cursor.fetchone()
                result = (result[0])

                if result < 1:
                    await ctx.send('You have to buy a fishing rod first')

                else:
                    fishtypes = [
                        'smallfish',
                        'mediumfish',
                        'largefish'
                    ]
                    fish = random.choice(fishtypes)
                    amount = 0

                    if fish == 'smallfish':
                        await ctx.send('You caught a **small fish**')

                    if fish == 'mediumfish':
                        await ctx.send('You caught a **small fish**')

                    if fish == 'largefish':
                        await ctx.send('You caught a **small fish**')

                    cursor.execute(f"INSERT INTO items (user_id, '{fish}') VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET '{fish}' = '{fish}' + ?;", [user, amount, amount])


        except asyncio.TimeoutError:
            await ctx.send('Well you didnt respond in time dumby')

        dbase.commit()
        dbase.close()

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Why do you want to be working so much GEEZ\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Slots
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slots(self, ctx, bet: int=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        bal = cursor.fetchone()

        user = ctx.author.id

        if bet is None:
            await ctx.send('You have to bet something dumby')

        else:
            if bal[0] < bet:
                await ctx.send('You dont have the money ot do that')

            else:
                if bet < 0:
                    await ctx.send('Just stop')
                
                else:
                    if bet < 50:
                        await ctx.send('Bet more than 50!')
                    
                    else:
                        if bet > 100000:
                            await ctx.send('Your bet has to be under 100k')

                        else:
                            outcome = [
                                '🤑',
                                '😢',
                                '😩',
                                '🥵',
                                '<:dankmerchants:829809749058650152>'
                            ]

                            outcome1 = random.choice(outcome)
                            outcome2 = random.choice(outcome)
                            outcome3 = random.choice(outcome)

                            if outcome1 == outcome2 == outcome3:
                                amount = int(bet * 3)

                                cursor.execute(f"INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

                                embed = discord.Embed(title='You Won!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou won: <:dankmerchants:829809749058650152> `{amount}`', color=0x00ff00)
                                await ctx.reply(embed=embed)

                            else:
                                if outcome1 == '<:dankmerchants:829809749058650152>' and outcome2 == '<:dankmerchants:829809749058650152>' and outcome3 == '<:dankmerchants:829809749058650152>':
                                    amount = int(bet * 10)

                                    cursor.execute(f"INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

                                    embed = discord.Embed(title='You Won The Jackpot!!!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou Won: <:dankmerchants:829809749058650152> `{amount}`', color=0x00ff00)
                                    await ctx.reply(embed=embed)

                                else:
                                    if outcome1 == outcome2 or outcome2 == outcome3 or outcome1 == outcome3:
                                        amount = int(bet * 1.5)

                                        cursor.execute(f"INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, amount, amount])

                                        embed = discord.Embed(title='You Won Some!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou Won: <:dankmerchants:829809749058650152> `{amount}`', color=0x00ff00)
                                        await ctx.reply(embed=embed)
                                    
                                    else:
                                        cursor.execute(f"INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, bet, bet])

                                        embed = discord.Embed(title='You Lost!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou lost: <:dankmerchants:829809749058650152> `{bet}`', color=0xff0000)
                                        await ctx.reply(embed=embed)

        dbase.commit()
        dbase.close()

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Stop using the slot machine before you breka it\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))
