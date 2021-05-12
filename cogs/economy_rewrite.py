from discord.ext.commands.errors import BadArgument
from items_bruni import currency
from items_bruni import economy_items
from discord.ext import commands
import discord
import sqlite3
import sys
import traceback
import random
from itertools import islice
from datetime import datetime

# TODO: ADD EXLUSIVE ITEMS INSIDE BUY COMMAND
# TODO: ADD ATTRIBUTES AND USAGES FOR ITEMS CATEGORY

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currency = currency
        self.economy_items = economy_items

    def user_exists(self, user_id):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute("SELECT balance FROM economy WHERE user_id == ?", [user_id])
        result = cursor.fetchone() is not None
        dbase.close()
        return result

    def add_user(self, user_id):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        tables_to_add = ["economy", "boxes", "items", "collectables", "materials", "multis", "tools"]
        
        for table in tables_to_add:
            cursor.execute("INSERT OR IGNORE INTO ? user_id VALUES ?", [user_id, table])
        
        dbase.commit()
        dbase.close()
    
    def beautify_number(self, num):
        return '{:,}'.format(num)

    def cog_check(self, ctx):
        if not self.user_exists(ctx.author.id):
            self.add_user(ctx.author.id)
        return True

    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, member: discord.Member = None):
        user = member or ctx.author

        if not self.user_exists(user.id): # if the persion is not in database
            self.add_user(user.id)
        
        amount = self.currency.get_amount(user.id)
        bal_embed = discord.Embed(
            title = f"{user.name}'s balance",
            description = f"**Balance:**\n{self.currency.emoji} {amount}",
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


    @commands.command()
    async def rich(self, ctx):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()

        cursor.execute("SELECT balance, user_id FROM economy ORDER BY balance DESC")
        richest = cursor.fetchmany(10)

        rich_embed = discord.Embed(
            title = "Richest People In Dank Merchants", 
            colour = 0x00ff00
        )

        embed_desc = ""
        dank_merchants = self.client.get_guild(784491141022220309)
        for index, user_info in enumerate(richest):
            member = dank_merchants.get_member(int(user_info[1]))
            embed_desc += f"**{index + 1}. {member.name}:** {self.currency.emoji} `{'{:,}'.format(user_info[0])}`\n"

        rich_embed.description = embed_desc
        await ctx.send(embed = rich_embed)

        dbase.close()

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, member: discord.Member = None, page: int = 1):
        item_limit_per_page = 5 # for displaying a maximum number of items in the inventory

        user = member or ctx.author

        if not self.user_exists(user.id): # if the persion is not in database
            self.add_user(user.id)

        inv_embed = discord.Embed(
            title = f"{user.name}’s Inventory" ,
            colour = 0x00ff00
        )

        user_items = self.economy_items.copy() # will be left with items that the user has
        for name, item in user_items.items():
            quantity = item.get_amount(user.id)
            if quantity == 0:
                del user_items[name]
            else:
                user_items[name] = quantity

        for name, item_count in dict(islice(user_items.items(), (page - 1) * 5, page *5)):
            inv_embed.add_field(
                name = f"{self.economy_items[name].emoji} __{self.economy_items[name].name}__",
                value = f"**{self.beautify_number(item_count)}** owned",
                inline = False
            )

        if inv_embed.fields == []:
            return await ctx.send(f"Page {page} doesn’t exist")
        
        total_pages = len(user_items) // item_limit_per_page + 1
        inv_embed.set_footer(text = f"Page {page} of {total_pages}")
        return await ctx.send(embed = inv_embed)

    @inventory.error
    async def inv_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("That isn't a valid user")
        
        if isinstance(error, BadArgument):
            return await ctx.send("You either specify a page or don't specify one at all")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @commands.command(aliases = ["store"])
    async def shop(self, ctx, *, item_or_page = None):
        is_item = False

        try:
            page = int(item_or_page)
        except ValueError:
            is_item = True
        
        if is_item:
            for name, item in self.economy_items.items():

                if item_or_page.lower().replace(" ", "") in name.lower().replace(" ", ""):

                    item_info_embed = discord.Embed(
                        title = f"{item.name} ({self.beautify_number(item.get_item_count(ctx.author.id))} owned)",
                        description = item.description,
                        colour = 0x00ff00
                    )
                    
                    if item.purchasable:
                        item_info_embed.add_field(
                            name = "Buy: ",
                            value = f"{self.currency.emoji} **{self.beautify_number(item.price)}**",
                            inline = False
                        )
                    else:
                        item_info_embed.add_field(
                            name = "Buy: ",
                            value = "This item cannot be bought",
                            inline = False
                        )
                    
                    if item.sellable:
                        item_info_embed.add_field(
                            name = "Sell: ",
                            value = f"{self.currency.emoji} **{self.beautify_number(item.sell_price)}**",
                            inline = False
                        )
                    else:
                        item_info_embed.add_field(
                            name = "Sell: ",
                            value = "This item cannot be sold",
                            inline = False
                        )

                    item_info_embed.set_thumbnail(item.image_url)

                    return await ctx.send(embed = item_info_embed)
            
            return await ctx.send("That's not a valid item")

        purchasable_items = [item for name,item in self.economy_items.items() if item.purchasable]

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
            shop_embed.descripton += f"{item.emoji} **{item.name}** - {self.currency.emoji} {self.beautify_number(item.price)}\n\n"
        shop_embed.set_footer(text = f"Page {page} of {pages_of_shop}")   

        return await ctx.send(embed = shop_embed) 

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, *item_and_count):
        if item_and_count == ():
            return await ctx.send("You need to specify an item to buy")

        try:
            count = int(item_and_count[0])
        except ValueError:
            count = 1
        finally:
            item = "".join(item_and_count[1:])

        if count < 1:
            return await ctx.send("You can't buy negative items, dummy")
        
        if item == "":
            return await ctx.send("You need to enter an item to buy, dummy")        

        purchasable_items = [name for name, item_class in self.economy_items.items() if item_class.purchasable]

        for name in purchasable_items:
            if item.lower() in name.replace(" ", ""):

                if self.currency.get_amount(ctx.author.id) < self.economy_items[name].price * count:
                    return await ctx.send("You don't have enough money for that LMAO")
                

                self.economy_items[name].purchase_items(ctx.author.id, count)
                return await ctx.send(f"Bought {count} {name}, paid {self.currency.emoji} {self.economy_items[name].price * count}")
        
        return await ctx.send("That wasn't a valid item to buy")

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    

    @commands.command()
    async def sell(self, ctx, *item_and_count):
        if item_and_count == ():
            return await ctx.send("You need to specify an item to sell")

        try:
            count = int(item_and_count[0])
        except ValueError:
            count = 1
        finally:
            item = "".join(item_and_count[1:])

        if count < 1:
            return await ctx.send("You can't sell negative items, dummy")
        
        if item == "":
            return await ctx.send("You need to enter an item to buy, dummy")        

        purchasable_items = [name for name,item_class in self.economy_items.items() if item_class.sellable]

        for name in purchasable_items:
            if item.lower() in name.replace(" ", ""):

                if self.economy_items[name].get_item_count(ctx.author.id) < count:
                    return await ctx.send("You literally don't have that many items smh")
                

                self.economy_items[name].sell_items(ctx.author.id, count)
                return await ctx.send(f"Sold {count} {name}, got {self.currency.emoji} {self.economy_items[name].price * count}")
        
        return await ctx.send("That wasn't a valid item to sell")
    

    @sell.error
    async def sell_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx, *item_and_count):
        if item_and_count == ():
            return await ctx.send("You need to specify an item to use")

        try:
            count = int(item_and_count[0])
        except ValueError:
            count = 1
        finally:
            item = "".join(item_and_count[1:])

        if count < 1:
            return await ctx.send("You can't use negative items, dummy")
        
        if item == "":
            return await ctx.send("You need to enter an item to use, dummy")
        
        for name, item_class in self.economy_items.items():
            if item.lower().replace(" ", "") in name.lower().replace(" ", ""):
                
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
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    
    @commands.command()
    async def give(self, ctx, member: discord.Member, amount: int):
        if member == ctx.author:
            return await ctx.send("Why would you want to give yourself money?")
        
        if amount <= 0:
            return await ctx.send("Key in a valid amount to enter")
        
        if self.currency.get_amount(ctx.author.id) < amount:
            return await ctx.send("You don't have enough money for that!")
        
        if not self.user_exists(member.id): # if the persion is not in database
            self.add_user(member.id)
        
        tax_rate = 8 # in percentages
        after_taxes = round(amount * (100-tax_rate)/100)

        self.currency.add(member.id, after_taxes)
        self.currency.subtract(ctx.author.id, amount)

        return await ctx.send(f"You gave {member.name} {self.currency.emoji} {after_taxes}, after a {tax_rate}% tax rate")


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
    
    @commands.command()
    async def gift(self, ctx, count: int, *item_and_member):    
        if item_and_member == () or len(item_and_member) < 2:
            return await ctx.send("It's `b!gift <amount> <item> <user>`")
        
        if count <= 0:
            return await ctx.send("Key in a valid number of items to gift")
        
        try:
            member = commands.MemberConverter(item_and_member[-1])
        except commands.errors.MemberNotFound:
            return await ctx.send("That's not a valid user")

        if not self.user_exists(member.id): # if the persion is not in database
            self.add_user(member.id)
        
        item = "".join(item_and_member[:-1])

        for name, item_class in self.economy_items.items():
            if item.lower() in name.lower().replace(" ", ""):
                
                if item_class.get_item_count(ctx.author.id) < count:
                    return await ctx.send("You don't have that many items")
                
                item_class.increase_item(member.id, count)
                item_class.decrease_item(ctx.author.id, count)

                return await ctx.send(f"You gave {member.name} {count} {item_class.name}")

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
    
    @commands.command()
    @commands.cooldown(1, 35, commands.BucketType.user)
    async def beg(self, ctx):
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
            'Tommy'
        ]

        doughnut_count = self.economy_items["Doughnut"].get_item_count(ctx.author.id)
        effective_mult = min(doughnut_count, 5) * 5 # maximum of 5 doughnuts with 5% each
        amount = round(random.randint(100, 1000) * (100 + effective_mult) / 100)

        self.currency.add(ctx.author.id, amount)

        response = f"You got {self.currency.emoji} **{amount}** from {random.choice(names)}"
        if effective_mult == 0:
            response += f"\nWith the help of {effective_mult // 5} doughnuts, you got {effective_mult}% more than you would have!"

        return await ctx.send(response)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    @commands.command()
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bet(self, ctx, bet_amount):
        if bet_amount.lower() in ("all", "max"):
            return await self.bet(ctx, min(self.currency.get_amount(ctx.author.id), 250000))
        
        try:
            bet_amount = int(bet_amount)
        except ValueError:
            return await ctx.send("You need to send a valid amount to bet")

        if bet_amount < 0:
            return await ctx.send("Key in a valid amount to bet")
        if bet_amount < 100:
            return await ctx.send(f"You can only bet a minimum of {self.currency.emoji} 100")
        if bet_amount > 250000:
            return await ctx.send(f"You can only bet a maximum of {self.currency.emoji} 250000 at once")

        if self.currency.get_amount(ctx.author.id) < bet_amount:
            return await ctx.send("You don't have enough money for that")
        
        doughnut_count = self.economy_items["Doughnut"].get_item_count(ctx.author.id)
        effective_mult = min(doughnut_count, 5) * 5 # maximum of 5 doughnuts with 5% each
        win = random.choice([True, False])

        if not win:
            self.currency.subtract(bet_amount)
            embed = discord.Embed(title = "Bet Results", description = "You lost", color = 0xff0000)
            embed.add_field(name = "You lost:", value = f"{self.currency.emoji} `{bet_amount}`")
            return await ctx.send(embed=embed)
        
        winnings = round(bet_amount * random.randint(50,150)/100 * (effective_mult + 100) / 100)
        
        
        # TODO: continue



    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            return await ctx.send(embed=embed)
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("You need to enter an amount to bet")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(economy(bot))
