import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import asyncio
import sqlite3
import random
from datetime import datetime
from items_bruni import economy_items, currency
from itertools import islice
import traceback
import sys

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
    async def inventory(self, ctx, member: discord.Member = None, page: int = 1):
        return await ctx.send("There's a bug in here for now... ")
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

        for name, item_count in dict(islice(user_items.items(), (page - 1) * 5, page *5)):
            inv_embed.add_field(
                name = f"{self.items[name].emoji} __{self.items[name].name}__",
                value = f"**{self.beautify_number(item_count)}** owned",
                inline = False
            )
        await ctx.send(str(dict(islice(user_items.items(), (page - 1) * 5, page *5))))

        if inv_embed.fields == []:
            return await ctx.send(f"Page {page} doesn’t exist")
        
        total_pages = len(user_items) // item_limit_per_page + 1
        inv_embed.set_footer(text = f"Page {page} of {total_pages}")
        return await ctx.send(embed = inv_embed)

    @inventory.error
    async def inv_error(self, ctx, error):
        await ctx.send(f"{type(error)} {error}")
        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.send("That isn't a valid user")
        
        if isinstance(error, BadArgument):
            return await ctx.send("You either specify a page or don't specify one at all")
        
        # print any other error
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    #Shop
    @commands.command(aliases=['store'])
    async def shop(self, ctx, item=None):
        #Page 1
        if item == '1' or item is None:
            embed = discord.Embed(title='Dank Merchants Shop', description='__**Shop Items:**__\n\n<:woodbox:830211928595890206> **Wood Loot Box** - <:dankmerchants:829809749058650152> 50,000\n\n<:ironbox:830197241934512188> **Iron Loot Box** - <:dankmerchants:829809749058650152> 100,000\n\n<:goldbox:830197220405805147> **Gold Loot Box** - <:dankmerchants:829809749058650152> 250,000\n\n<:diamondbox:830197220007477259> **Diamond Loot Box** - <:dankmerchants:829809749058650152> 500,000\n\n<:emeraldbox:830216613755486229> **Emerald Loot Box** - <:dankmerchants:829809749058650152> 1,000,000', color=0x00ff00)
            embed.set_footer(text='Page 1-1')
            await ctx.send(embed=embed)

        '''
        Boxes
        '''
        if item == 'woodbox' or item == 'wooden' or item == 'wdb':
            embed = discord.Embed(title='Wooden Box', description='A basic wooden box that could find you some loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830211928595890206.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **50,000**')
            await ctx.send(embed=embed)

        if item == 'ironbox' or item == 'irb':
            embed = discord.Embed(title='Iron Box', description='A solid iron box probally has some good stuff in it', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197241934512188.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)

        if item == 'goldbox' or item == 'gdb':
            embed = discord.Embed(title='Gold Box', description='A solid gold box that must have good loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220405805147.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **250,000**')
            await ctx.send(embed=embed)

        if item == 'diamondbox' or item == 'dib':
            embed = discord.Embed(title='Diamond Box', description='A solid diamond box that is bound to have good loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830197220007477259.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **500,000**')
            await ctx.send(embed=embed)

        if item == 'emeraldbox' or item == 'emb':
            embed = discord.Embed(title='Emerald Box', description='The best box of them all that will have the best loot', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/830216613755486229.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **1,000,000**')
            await ctx.send(embed=embed)

        '''
        Resources
        '''
        if item == 'wood' or item == 'woo':
            embed = discord.Embed(title='Wood', description='Wood can be used for many things', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835262637851541555.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **NONE**')
            await ctx.send(embed=embed)

        if item == 'iron' or item == 'iro':
            embed = discord.Embed(title='Iron', description='Used to make medal could probally sell for some money', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/834958446906441789.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **NONE**')
            await ctx.send(embed=embed)

        if item == 'gold' or item == 'gol':
            embed = discord.Embed(title='Gold', description='A pretty expensive mineral', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/834958470955532338.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **NONE**')
            await ctx.send(embed=embed)

        if item == 'diamond' or item == 'dia':
            embed = discord.Embed(title='Diamond', description='A blue gem worth some money', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/834958491315339294.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **NONE**')
            await ctx.send(embed=embed)

        if item == 'emerald' or item == 'eme':
            embed = discord.Embed(title='Emerald', description='A green gem worth a bit of money', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/834958503369637941.png?v')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **NONE**')
            await ctx.send(embed=embed)

        '''
        Tools
        '''
        if item == 'woodpick' or item == 'wdp':
            embed = discord.Embed(title='Wooden Pickaxe', description='The most basic pickaxe you have ever seen', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835505500035612772.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **10,000**')
            await ctx.send(embed=embed)

        if item == 'ironpick' or item == 'irp':
            embed = discord.Embed(title='Iron Pickaxe', description='An entry level pickaxe', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835505509716197437.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **50,000**')
            await ctx.send(embed=embed)

        if item == 'goldpick' or item == 'gdp':
            embed = discord.Embed(title='Gold Pickaxe', description='A very fast pickaxe', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835505519468740608.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)

        if item == 'diamondpick' or item == 'dmp':
            embed = discord.Embed(title='Diamond Pickaxe', description='One of the best pickaxes', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835505528913264661.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **250,000**')
            await ctx.send(embed=embed)

        if item == 'emeraldpick' or item == 'edp':
            embed = discord.Embed(title='Emerald Pickaxe', description='The best of the pickaxes', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/835505536744161330.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **500,000**')
            await ctx.send(embed=embed)

        if item == 'gun':
            embed = discord.Embed(title='Gun', description='You can use it to go hunting', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/836051483224309790.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **100,000**')
            await ctx.send(embed=embed)

        if item == 'fishingrod' or item == 'fishingpole' or item == 'fishrod' or item == 'fsd' or item == 'pole':
            embed = discord.Embed(title='Emerald Pickaxe', description='Have a nice peaceful time while fishing', color=0x00ff00)
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/836051493744148561.png?v=1')
            embed.add_field(name='Buy:', value='<:dankmerchants:829809749058650152> **75,000**')
            await ctx.send(embed=embed)

    #Buy
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, item=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        client = self.client
        member = ctx.author
        user = ctx.author.id

        item.lower()

        cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        bal = (result[0])

        if item == None:
            await ctx.send('You actully have to name a item to buy it (0)_(0)')
        
        '''
        EXCLUSIVE ITEMS
        '''
        date = str(datetime.now())[5:10]

        if item == 'bruni' or item == 'brunibox' or item == 'brunisbox':
            if date == '08-22':
                await ctx.send("Congrats! You guessed bruni's birthday correct and you got some stuff for her birthday!\nBruni's Box: `1`")

            else:
                await ctx.send(f"Nope! It is not bruni's birthday")


        if item == 'wiggle' or item == 'wigglebox' or item == 'wigglesbox':
            if date == '03-07':
                await ctx.send("Congrats! You guessed Wiggle's birthday correct and you got some stuff for his birthday!\nBruni's Box: `1`")

            else:
                await ctx.send(f"Nope! It is not Wiggle's birthday")

        '''
        BOXES
        '''
        if item == 'wooden' or item == 'wood' or item == 'woo':
            if bal >= 50000:
                amount = 50000
                box = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, woodbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodbox = woodbox + ?;", [user, box, box])

                await ctx.send('Enjoy your wooden box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'iron' or item == 'iro':
            if bal >= 100000:
                amount = 100000
                box = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox + ?;", [user, box, box])

                await ctx.send('Enjoy your iron box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'gold' or item == 'gol':
            if bal >= 250000:
                amount = 250000
                box = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, goldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldbox = goldbox + ?;", [user, box, box])

                await ctx.send('Enjoy your gold box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'diamond' or item == 'dia':
            if bal >= 500000:
                amount = 500000
                box = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox + ?;", [user, box, box])

                await ctx.send('Enjoy your diamond box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'emerald' or item == 'eme':
            if bal >= 1000000:
                amount = 1000000
                box = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox + ?;", [user, box, box])

                await ctx.send('Enjoy your emerald box')

            else:
                await ctx.send('You dont have enough money to buy that!')

        '''
        TOOLS
        '''
        if item == 'woodpick' or item == 'wdp':
            if bal >= 10000:
                amount = 10000
                pick = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, woodpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET woodpick = woodpick + ?;", [user, pick, pick])

                await ctx.send('Enjoy wood pickaxe')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'ironpick' or item == 'irp':
            if bal >= 50000:
                amount = 50000
                pick = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, ironpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironpick = ironpick + ?;", [user, pick, pick])

                await ctx.send('Enjoy iron pickaxe')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'goldpick' or item == 'gdp':
            if bal >= 100000:
                amount = 100000
                pick = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, goldpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET goldpick = goldpick + ?;", [user, pick, pick])

                await ctx.send('Enjoy gold pickaxe')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'diamondpick' or item == 'dmp':
            if bal >= 250000:
                amount = 250000
                pick = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, diamondpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondpick = diamondpick + ?;", [user, pick, pick])

                await ctx.send('Enjoy diamond pickaxe')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'emeraldpick' or item == 'edp':
            if bal >= 500000:
                amount = 500000
                pick = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, emeraldpick) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldpick = emeraldpick + ?;", [user, pick, pick])

                await ctx.send('Enjoy emerald pickaxe')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'gun':
            if bal >= 100000:
                amount = 100000
                gun = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, gun) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gun = gun + ?;", [user, gun, gun])

                await ctx.send('Enjoy gun')

            else:
                await ctx.send('You dont have enough money to buy that!')

        if item == 'fishingrod' or item == 'fishingpole' or item == 'fishrod' or item == 'fsd' or item == 'pole':
            if bal >= 75000:
                amount = 75000
                pole = 1

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance - ?;", [user, amount, amount])
                cursor.execute("INSERT INTO tools (user_id, gun) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gun = gun + ?;", [user, pole, pole])

                await ctx.send('Enjoy fishing pole')

            else:
                await ctx.send('You dont have enough money to buy that!')

        dbase.commit()
        dbase.close()

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)

    #Use
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx, item=None):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

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
                
                coins = random.randint(12500, 25000)
                appleamount = random.randint(0, 5)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO items (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples: `{appleamount}`***')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Iron Box
        if item == 'iron':
            cursor.execute(f"SELECT ironbox FROM boxes WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, ironbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET ironbox = ironbox - ?;", [user, box, box])

                coins = random.randint(25000, 50000)
                appleamount = random.randint(0, 10)
                duckamount = random.randint(1, 5)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO items (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
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

                coins = random.randint(50000, 100000)
                appleamount = random.randint(0, 15)
                duckamount = random.randint(1, 10)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO items (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\nCoins: `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Diamond Box
        if item == 'diamond':
            cursor.execute(f"SELECT diamondbox FROM boxes WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, diamondbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamondbox = diamondbox - ?;", [user, box, box])

                coins = random.randint(100000, 250000)
                appleamount = random.randint(1, 25)
                duckamount = random.randint(1, 25)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO items (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        #Emerald Box
        if item == 'emerald':
            cursor.execute(f"SELECT emeraldbox FROM boxes WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            result = (result[0])

            if result > 0:
                box = 1
                cursor.execute("INSERT INTO boxes (user_id, emeraldbox) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emeraldbox = emeraldbox - ?;", [user, box, box])

                coins = random.randint(250000, 500000)
                appleamount = random.randint(1, 50)
                duckamount = random.randint(1, 10)
                donutamount = random.randint(0, 1)

                cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, coins, coins])
                cursor.execute("INSERT INTO items (user_id, apple) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET apple = apple + ?;", [user, appleamount, appleamount])
                cursor.execute("INSERT INTO items (user_id, duck) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET duck = duck + ?;", [user, duckamount, duckamount])
                cursor.execute("INSERT INTO multis (user_id, doughnut) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET doughnut = doughnut + ?;", [user, donutamount, donutamount])

                await ctx.send(f'Box Contents:\n***Coins:*** `{coins}`\n***Apples:*** `{appleamount}`\n***Ducks:*** `{duckamount}`\n***Donuts:*** `{donutamount}`')

            else:
                await ctx.send('Hate to break it to you but you dont really own one of those')

        dbase.commit()
        dbase.close()

    @use.error
    async def use_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f'WOAH There Slow It Down!',description=f'Try again in `{error.retry_after:.2f}`s', color=0x00ff00)
            await ctx.send(embed=embed)


    #Sell
    @commands.command()
    async def sell(self, ctx, item=None, amount=1):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id
        
        if item is None:
            await ctx.send('What are you trying to sell? LMAO')

        else:
            if amount < 0:
                await ctx.send('Dont even think about it')

            else:
                if item == 'wood':
                    cursor.execute(f"SELECT wood FROM materials WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    result = int(result[0])

                    if amount > result:
                        await ctx.send(f'You dont even have that many wood you have `{result}`')

                    else:
                        cursor.execute("INSERT INTO materials (user_id, wood) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET wood = wood - ?;", [user, amount, amount])
                        total = amount * 50
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, total, total])

                        await ctx.send(f'You sold **{amount} {item}** and made <:dankmerchants:829809749058650152> `{total}`')

                if item == 'iron':
                    cursor.execute(f"SELECT iron FROM materials WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    result = int(result[0])

                    if amount > result:
                        await ctx.send(f'You dont even have that many iron you have `{result}`')

                    else:
                        cursor.execute("INSERT INTO materials (user_id, iron) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET iron = iron - ?;", [user, amount, amount])
                        total = amount * 100
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, total, total])

                        await ctx.send(f'You sold **{amount} {item}** and made <:dankmerchants:829809749058650152> `{total}`')

                if item == 'gold':
                    cursor.execute(f"SELECT gold FROM materials WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    result = int(result[0])

                    if amount > result:
                        await ctx.send(f'You dont even have that many gold you have `{result}`')

                    else:
                        cursor.execute("INSERT INTO materials (user_id, gold) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gold = gold - ?;", [user, amount, amount])
                        total = amount * 250
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, total, total])

                        await ctx.send(f'You sold **{amount} {item}** and made <:dankmerchants:829809749058650152> `{total}`')

                if item == 'diamond':
                    cursor.execute(f"SELECT diamond FROM materials WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    result = int(result[0])

                    if amount > result:
                        await ctx.send(f'You dont even have that many diamond you have `{result}`')

                    else:
                        cursor.execute("INSERT INTO materials (user_id, diamond) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET diamond = diamond - ?;", [user, amount, amount])
                        total = amount * 500
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, total, total])

                        await ctx.send(f'You sold **{amount} {item}** and made <:dankmerchants:829809749058650152> `{total}`')

                if item == 'emerald':
                    cursor.execute(f"SELECT emerald FROM materials WHERE user_id = '{ctx.author.id}'")
                    result = cursor.fetchone()
                    result = int(result[0])

                    if amount > result:
                        await ctx.send(f'You dont even have that many emerald you have `{result}`')

                    else:
                        cursor.execute("INSERT INTO materials (user_id, emerald) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET emerald = emerald - ?;", [user, amount, amount])
                        total = amount * 1000
                        cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?;", [user, total, total])

                        await ctx.send(f'You sold **{amount} {item}** and made <:dankmerchants:829809749058650152> `{total}`')

        dbase.commit()
        dbase.close()

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
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        user = ctx.author.id

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

                        if bet <= 250000:
                            new_bet = bet * 1.5
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
                            await ctx.reply('Woah there the max you can bet is 250k at a time!')

        dbase.commit()
        dbase.close()

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
