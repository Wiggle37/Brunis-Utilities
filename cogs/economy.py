from types import new_class
import discord
from discord import *
from discord.ext import commands
from discord.ext.commands import *
from discord.errors import *
from discord.ext.commands.core import *
import asyncio
import sqlite3
import random
from datetime import datetime
from itertools import islice
import traceback
import sys
import typing

from items_bruni import *

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.items = economy_items
        self.currency = currency
        self.memberConverter = commands.MemberConverter()

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

    async def no_general(self, ctx):
        channel = ctx.channel
        if channel.id == 784491141022220312:
            return True

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
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [message.author.id, 500, 500])
            cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [message.author.id, 0, 0])
            cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [message.author.id, 0, 0])
            cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [message.author.id, 0, 0])
            cursor.execute("INSERT INTO materials (user_id, wood) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wood = wood + ?;", [message.author.id, 0, 0])
            cursor.execute("INSERT INTO collectables (user_id, wiggle) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wiggle = wiggle + ?;", [message.author.id, 0, 0])
            cursor.execute("INSERT INTO tools (user_id, woodpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodpick = woodpick + ?;", [message.author.id, 0, 0])

        dbase.commit()
        dbase.close()

    '''
    General
    '''
    @commands.command()
    async def multi(self, ctx):
        multi = multis.get_multi(ctx.author.id)
        await ctx.send(f'Your curent multiplier is: **{float(multi * 100)}%**')

    #Balance
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member = None):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")
               
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
    @commands.command(aliases=['lb'])
    async def rich(self, ctx):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()

        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

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
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        item_limit_per_page = 5

        user = member or ctx.author

        inv_embed = discord.Embed(
            title = f"{user.name}’s Inventory" ,
            colour = 0x00ff00
        )

        user_items = self.items.copy()
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
        
        total_pages = len(user_items) // item_limit_per_page + 1 * (len(user_items) % item_limit_per_page != 0)
        inv_embed.set_footer(text = f"Page {page} of {total_pages}")
        return await ctx.send(embed = inv_embed)

    #Shop
    @commands.command(aliases = ["store"])
    async def shop(self, ctx, page: typing.Optional[int], *, item_name = None):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

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
        pages_of_shop = len(purchasable_items) // item_limit_per_page + 1 * (len(purchasable_items) % item_limit_per_page != 0)

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
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")
            
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
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

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
    async def use(self, ctx, count: typing.Optional[int] = 1, *, item_name):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

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
    async def give(self, ctx, member: discord.Member, amount: int):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        if member == ctx.author:
            return await ctx.send("Why would you want to give yourself money?")
        
        if amount <= 0:
            return await ctx.send("Key in a valid amount to enter")
        
        if self.currency.get_amount(ctx.author.id) < amount:
            return await ctx.send("You don't have enough money for that!")
        
        tax_rate = 8
        after_taxes = round(amount * (100-tax_rate)/100)

        self.currency.add(member.id, after_taxes)
        self.currency.subtract(ctx.author.id, amount)

        return await ctx.send(f"You gave **{member.name}** {self.currency.emoji} **{self.beautify_number(after_taxes)}**, after a {tax_rate}% tax rate")

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("It's `b!give <user> <amount>`")
        
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("That isn't a valid user")
        
        if isinstance(error, BadArgument):
            return await ctx.send("You have to type in an amount to give")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    #Gift
    @commands.command()
    async def gift(self, ctx, count: int, *item_and_member):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        if item_and_member == () or len(item_and_member) < 2:
            return await ctx.send("It's `b!gift <amount> <item> <user>`")
        
        if count <= 0:
            return await ctx.send("Key in a valid number of items to gift")
        
        try:
            member = await self.memberConverter.convert(ctx, item_and_member[-1])
        except commands.errors.MemberNotFound:
            return await ctx.send("That's not a valid user")
        
        item_name = "".join(item_and_member[:-1])

        for name, item_class in self.items.items():
            if item_name.lower().replace(" ", "") not in name.lower().replace(" ", ""):
                continue

            if item_class.get_item_count(ctx.author.id) < count:
                return await ctx.send("You don't have that many items")
            
            item_class.increase_item(member.id, count)
            item_class.decrease_item(ctx.author.id, count)

            return await ctx.send(f"You gave **{member.name}** {self.beautify_number(count)} {item_class.emoji} {item_class.name}")

        return await ctx.send("That's not a valid item")


    @gift.error
    async def gift_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("It's `b!gift <amount> <item> <user>`")
        
        if isinstance(error, BadArgument):
            return await ctx.send("You have to type in a number of items you want to give")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    '''
    Money Making
    '''
    #Beg
    @commands.command()
    @commands.cooldown(1, 35, commands.BucketType.user)
    async def beg(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        amount = random.randint(100, 1000)

        names = [
            'Lily',
            'Darkside',
            'Dark',
            'Neon',
            'PHYCHO',
            'Dank Mazen',
            'Bruni',
            'Wiggle',
            'The Orange Fresh',
            'Skeppy',
            'Copi',
            'Papercat',
            'Ethereal',
            'Dukie',
            'Adit',
            'Tommy',
            'Julesi',
            'Firecracker',
            'DM WIGGLE FOR NITRO YOU JUST WON SOME EPIC NITRO'
        ]

        multi = multis.get_multi(ctx.author.id)
        new_amount = int(amount * (1 + multi))

        self.currency.add(ctx.author.id, new_amount)

        await ctx.reply(f"{random.choice(names)} gave you {self.currency.emoji} **{int(new_amount)}** after a {multi * 100}% multi")

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    
    #Bet
    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bet(self, ctx, bet):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        if bet.lower() == "max" or bet.lower() == "all":
            # typecasting amount to string to preserve invocation style
            return await self.bet(ctx, str(min(500000, self.currency.get_amount(ctx.author.id))))

        bet = self.is_valid_int(bet)
        if bet is False:
            return await ctx.send('Please enter a valid number')

        if bet > 500000:
            return await ctx.send('The max bet is 500k at a time')

        bal = self.currency.get_amount(ctx.author.id)
        if bal < bet:
            return await ctx.send("You don't even have enough money to do that")
        
        win = random.choice([True, False])
        if win:
            amount = bet * 1.3
            multi = multis.get_multi(ctx.author.id)
            new_amount = int(amount * (1 + multi))
            self.currency.add(ctx.author.id, new_amount)

            bet_embed = discord.Embed(title='Bet Results', description='You Won!', color=0x00ff00)
            bet_embed.add_field(name='You Won:', value=f'{self.currency.emoji} `{self.beautify_number(int(new_amount))}`')

        if not win:
            self.currency.subtract(ctx.author.id, bet)
            bet_embed = discord.Embed(title='Bet Results', description='You lost, sucks', color=0xff0000)
            bet_embed.add_field(name='You lost:', value=f'{self.currency.emoji} `{self.beautify_number(int(bet))}`')

        return await ctx.reply(embed = bet_embed)
    
    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'If I let you go now you wouldnt have much money\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Slots
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slots(self, ctx, bet = None):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        if bet.lower() == "max" or bet.lower() == "all":
            # typecasting amount to string to preserve invocation style
            return await self.slots(ctx, str(min(100000, self.currency.get_amount(ctx.author.id))))

        bal = self.currency.get_amount(ctx.author.id)
        multi = multis.get_multi(ctx.author.id)
        bet = self.is_valid_int(bet)
        if bet == False:
            await ctx.send('Thats not a valid number')

        elif bet > 100000:
            return await ctx.send('The max you can bet is 100k at a time!')

        elif bal < bet:
            return await ctx.send('Yeh so you dont really have enough money to do that there')

        else:
            outcome1 = random.choice(['👑', '😩', '🥵', '🍔', '<:dankmerchants:829809749058650152>'])
            outcome2 = random.choice(['👑', '😩', '🥵', '🍔', '<:dankmerchants:829809749058650152>'])
            outcome3 = random.choice(['👑', '😩', '🥵', '🍔', '<:dankmerchants:829809749058650152>'])
            win = False

            if outcome1 == outcome2 == outcome3:
                amount = int(bet * 5)
                new_amount = int(multi * (1 + multi))
                self.currency.add(ctx.author.id, new_amount)
                win = True
                    
                embed = discord.Embed(title='You Won!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou won: {self.currency.emoji} `{new_amount}`', color=0x00ff00)

            elif outcome1 == outcome2 or outcome1 == outcome2 or outcome1 == outcome3 or outcome2 == outcome3:
                amount = int(bet * 1.5)
                new_amount = int(amount * (1 + multi))
                self.currency.add(ctx.author.id, new_amount)
                win = True

                embed = discord.Embed(title='You Won Some!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou Won: {self.currency.emoji} `{new_amount}`', color=0xffff00)

            elif outcome1 == '<:dankmerchants:829809749058650152>' and outcome2 == '<:dankmerchants:829809749058650152>' and outcome3 == '<:dankmerchants:829809749058650152>':
                amount = int(bet * 10)
                new_amount = int(amount * (1 + multi))
                self.currency.add(ctx.author.id, new_amount)
                win = True

                embed = discord.Embed(title='You Won The Jackpot!!!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou Won: {self.currency.emoji} `{new_amount}`')

            elif win == False:
                self.currency.subtract(ctx.author.id, bet)

                embed = discord.Embed(title='You Lost!', description=f'Outcome:\n{outcome1} {outcome2} {outcome3}\n\nYou Lost: {self.currency.emoji} `{bet}`', color=0xff000)

            await ctx.reply(embed=embed)
    
    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'If I let you go now you wouldnt have much money\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    
    #Work
    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        response = 'You got some stuff for working:'
        possible_items = [
            dukesBadge,
            darksbadge,
            snowflake,
            doughnut,
            iphone,
            goldBox
        ]

        item = random.choice(possible_items)
        item.increase_item(ctx.author.id, 1)
        response += f"\n***{item.emoji} {item.name}:*** `1`"

        return await ctx.send(response)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'No, stop being a work addict\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Mine
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def mine(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        await ctx.send('Wiggle is working on it')
    
    #Dig
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dig(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        shovelcheck = shovel.get_item_count(ctx.author.id)
        if shovelcheck < 1:
            await ctx.send('You need to buy a shovel to do this, run the command `b!buy 1 shovel`')

        else:
            amount = random.randint(1, 5000)
            item = random.choice([butilCoin, ironBox, goldBox, apple, emerald])
            itemamount = random.randint(1, 3)

            item.increase_item(ctx.author.id, itemamount)
            self.currency.add(ctx.author.id, amount)

            await ctx.send(f'You went digging in the dirt and found {itemamount} {item.emoji} {item.name} and {self.currency.emoji} {amount}')
    
    @dig.error
    async def dig_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Chop
    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def chop(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        axecheck = axe.get_item_count(ctx.author.id)
        if axecheck < 1:
            await ctx.send('You still need to buy an an axe, to do that run the command `b!buy 1 axe`')

        else:
            amount = random.randint(1, 7)
            wood.increase_item(ctx.author.id, amount)

            await ctx.send(f'You went to go chop down some trees and got {amount} {wood.emoji} {wood.name}')

    @chop.error
    async def chop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'No stop choping the trees before you are all tired out\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Hunt
    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def hunt(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        def check(m):
            return m.content == "hello" and m.channel == m.channel

        guncheck = gun.get_item_count(ctx.author.id)
        if guncheck < 1:
            await ctx.send('You need to buy a gun first! `b!buy 1 gun`')

        else:
            event = random.choice([True, False])
            if event:
                await ctx.send(f"OH NO THERE WAS A WILD {random.choice(['Goose', 'Duck', 'Chicken'])} came to woop you, QUICK what do you do?\n`1.` Shoot it and have a chance of living and gettings some loot\n`2.` Run away like a baby and get nothing")
                msg = await self.client.wait_for("message", check=check)

                if msg.clean_content.lower() == 'shoot':
                    action = random.choice(['hit', 'missed'])

                    if action == 'hit':
                        animal = random.choice([duck, goose, chicken])
                        animal.increase_item(ctx.author.id, 3)
                        await ctx.send(f'You hit the shot and got 3 {animal.name} {animal.name}s')

                    if action == 'missed':
                        await ctx.send("You missed your shot but the animal didn's care about you so you lost nothing")

                if msg.clean_content.lower() == 'run':
                    await ctx.send('You ran away like a baby and got nothing, LOL')

                elif msg.clean_content.lower() != 'shoot' or msg.clean_content.lower() != 'run':
                    amount = gun.get_item_count(ctx.author.id)
                    gun.decrease_item(ctx, amount)
                    await ctx.send("You didn't chose a valid option so you lost you all of your guns because you lost the fight")

            if not event:
                animal = random.choice([duck, goose, chicken])
                animal.increase_item(ctx.author.id, 1)
                await ctx.send(f'There were no problems along the way and you hunted in peace and got 1 {animal.emoji} {animal.name}')

    @hunt.error
    async def hunt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'No stop hunting before you are all tired out\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Fish
    @commands.command()
    @commands.cooldown(1, 15, BucketType.user)
    async def fish(self, ctx):
        channel = await self.no_general(ctx)
        if channel:
            return await ctx.send("Please don't use commands here please go to <#830867486769283072> instead")

        rodcheck = fishingRod.get_item_count(ctx.author.id)
        if rodcheck < 1:
            await ctx.send("Buy a fishing rob by running the command: `b!buy 1 pole`")

        else:
            amount = random.randint(1, 5)
            fishtype = random.choice([smallFish, mediumFish, largeFish])
            fishtype.increase_item(ctx.author.id, amount)

            await ctx.send(f'You went fishing and got {fishtype.emoji} {fishtype.name}')

    @fish.error
    async def fish_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'No stop fish before you are all tired out\nTry again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))