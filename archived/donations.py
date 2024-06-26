import discord
from discord.ext import commands

import aiohttp
import motor
import motor.motor_asyncio
from datetime import datetime

from config import *
from buttons import *

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.motor_session = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://mainHost:TStB72SYJGmte1MC@brunis-utilities.okced.mongodb.net/donations?retryWrites=true&w=majority')
        self.db = self.motor_session.donations
        self.categories = ['giveaway', 'heist', 'event', 'special', 'money']

    '''
    Donations
    '''
    async def get_required_roles(self, ctx, guild):
        self.db.guild_config.find_one()

    async def add_roles(self, ctx, user: discord.Member):
        user_roles_id = [role.id for role in user.roles]

        total = await self.get_amount(ctx, user)

        roles_ = self.db.guild_config.find_one({"_id": ctx.guild.id})
        donors_roles = roles_["donation_roles"]

        roles_added = []
        for amount, role_id in donors_roles.items():
            if total < amount:
                break

            if role_id in user_roles_id:
                continue

            role = discord.utils.find(lambda r: r.id == role_id, ctx.guild.roles)
            await user.add_roles(role)
            roles_added.append(role.name)

        if roles_added != []:
            return await ctx.send(f"**{user.name}** now has the role(s): `{', '.join(roles_added)}`! Tysm for donating!")
    def beautify_numbers(self, num):
        return "{:,}".format(num)

    async def get_user(self, ctx, user: discord.Member):
        db = self.motor_session.donations
        collection = db[str(ctx.guild.id)]

        e = await collection.find_one({"_id": user.id})
        if e is None:
            await collection.insert_one({"_id": user.id, "giveaway": 0, "heist": 0, "event": 0, "special": 0, "money": 0})

    async def get_user_amount(self, ctx, user: discord.Member):
        db = self.motor_session.donations
        collection = db[str(ctx.guild.id)]
        await self.get_user(ctx, user)

        return await collection.find_one({"_id": user.id})

    async def get_guild_config(self, ctx, guild):
        collection = self.db['guild_config']
        return await collection.find_one({"_id": ctx.guild.id})

    def is_valid_int(self, amount):
        try:
            float(amount.replace("m","").replace("k",""))
            return int(eval(amount.replace("k","e3").replace("m", "e6")))
            
        except ValueError:
            return False

    def embed(self, ctx, member: discord.Member, amount: int, category: int):
        e = {0: 'giveaway', 1: 'heist', 2: 'event', 3: 'special', 4: 'money'}
        currency = '⏣'
        if category == 4:
            currency = '$'
        if category not in e:
            raise IndexError(f'No found category found for "{category}"')

        embed = discord.Embed(title=f'Donations Updated For __{member.name}__', description=f'**User:** {member.mention}({member.id})\n**Amount:** `{currency}{self.beautify_numbers(amount)}`')
        embed.set_footer(text=f'Donations Updated By: {ctx.author.id}')
        return embed

    # Set-Up Donations
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def setup(self, ctx):
        db = self.motor_session.donations
        collections = await self.db.list_collection_names()

        if str(ctx.guild.id) in collections:
            return await ctx.send('Your server is already setup, there is no need to run this command again')
        
        collection = db[f'{ctx.guild.id}']
        guild_config = db['guild_config']
        await guild_config.insert_one({"_id": ctx.guild.id, "giveaway_ids": [], "heist_ids": [], "event_ids": [], "special_ids": [], "money_ids": [], "donation_roles": {}})
        await collection.insert_one({"_id": ctx.author.id, "giveaway": 0, "heist": 0, "event": 0, "special": 0, "money": 0})
        await ctx.send(f'Guild added to database, to edit who can use commands use `b!donation_config`')

    # Donation Config
    @commands.group(name='donation_config', invoke_without_command=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def donation_config(self, ctx):
        info = await self.get_guild_config(ctx, ctx.guild)
        collections = await self.db.list_collection_names()
        if str(ctx.guild.id) not in collections:
            return await ctx.send(f'This guild is not currently setup, to setup the guild please run the command `b!setup`')

        embed = discord.Embed(
            title='Donation Config', 
            description=(
                f'Giveaway Access: {", ".join([discord.utils.get(ctx.guild.roles, id = id).name for id in info["giveaway_ids"]])} \
                \nHeist Access: {", ".join([discord.utils.get(ctx.guild.roles, id = id).name for id in info["heist_ids"]])} \
                \nEvent Access: {", ".join([discord.utils.get(ctx.guild.roles, id = id).name for id in info["event_ids"]])} \
                \nSpecial Access: {", ".join([discord.utils.get(ctx.guild.roles, id = id).name for id in info["special_ids"]])} \
                \nMoney Access: {", ".join([discord.utils.get(ctx.guild.roles, id = id).name for id in info["money_ids"]])}'),
            color=0x9b59b6
            )

        await ctx.send(embed=embed)

    '''

    @donation_config.group(invoke_without_command=True)
    async def giveaway(self, ctx):
        await ctx.send('Please provide an action to complete either add or remove')
    @giveaway.command()
    async def add(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` added for managing giveaway donations')
    @giveaway.command()
    async def remove(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` removed for managing giveaway donations')

    @donation_config.group(invoke_without_command=True)
    async def heist(self, ctx):
        await ctx.send('Please provide an action to complete either add or remove')
    @heist.command()
    async def add(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` added for managing heist donations')
    @heist.command()
    async def remove(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` removed for managing heist donations')

    @donation_config.group(invoke_without_command=True)
    async def event(self, ctx):
        await ctx.send('Please provide an action to complete either add or remove')
    @event.command()
    async def add(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` added for managing event donations')
    @event.command()
    async def remove(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` removed for managing event donations')

    @donation_config.group(invoke_without_command=True)
    async def special(self, ctx):
        await ctx.send('Please provide an action to complete either add or remove')
    @special.command()
    async def add(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` added for managing special donations')
    @special.command()
    async def remove(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` removed for managing special donations')

    @donation_config.group(invoke_without_command=True)
    async def money(self, ctx):
        await ctx.send('Please provide an action to complete either add or remove')
    @money.command()
    async def add(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` added for managing money donations')
    @money.command()
    async def remove(self, ctx, role: discord.Role):
        self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"giveaway_ids": role.id}})
        await ctx.send(f'Role `{role.name}` removed for managing money donations')

    '''

    # Donation Roles
    @commands.group(invoke_without_command=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def donation_roles(self, ctx):
        collection = self.db.guild_config
        info = await collection.find_one({"_id": ctx.guild.id})
        roles = ''
        for amount, role in (sorted(info["donation_roles"].items(), key=lambda x: int(x[0]))):
            roles += f'**{self.beautify_numbers(int(amount))}:** `{discord.utils.get(ctx.guild.roles, id=role).name}`\n'
            
        embed = discord.Embed(title='Donation Roles', description=roles)
        await ctx.send(embed=embed)

    @donation_roles.command()
    async def add(self, ctx, amount: str, role: discord.Role):
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send('Please provide a valid amaount')
        
        collection = self.db.guild_config
        await collection.update_one({"_id": ctx.guild.id}, {"$set": {f'donation_roles.{str(amount)}': role.id}})
        await ctx.send(f'Donation role added. Amount: `{self.beautify_numbers(amount)}`, Role: `{role.name}`')

    @donation_roles.command()
    async def remove(self, ctx, amount: str):
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send('Please provide a valid amaount')
        
        collection = self.db.guild_config
        info = await collection.find_one({"_id": ctx.guild.id})
        await collection.update_one({"_id": ctx.guild.id}, {"$unset": {f"donation_roles.{str(amount)}": info["donation_roles"][str(amount)]}})
        await ctx.send(f'Donation role removed for `{self.beautify_numbers(amount)}`')
    
    # Check Donations
    @commands.command(name='e', description='Check your donations for the current server')
    @commands.has_guild_permissions(send_messages=True)
    async def dd(self, ctx, member: discord.Member=None):
        collection = self.db[str(ctx.guild.id)]
        member = member or ctx.author
        await self.get_user(ctx, member)
        info = await collection.find_one({"_id": member.id})

        embed = discord.Embed(title=f'{member}\'s Donations', color=discord.Color.dark_purple())
        embed.description = (
            f'\
            \nGiveaway: `⏣{info["giveaway"]}` \
            \nHeist: `⏣{info["heist"]}` \
            \nEvent: `⏣{info["event"]}` \
            \nSpecial: `⏣{info["special"]}` \
            \nMoney: `${info["money"]}`'

        )
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='This is a rewrite version of donations all changes are NOT final')
        await ctx.send(embed=embed)







    '''
    Add Donations
    '''
    @commands.group(name='add_donations', description='Add donations to a user', aliases=['ad', 'da'], invoke_without_command=True)
    async def add_donations(self, ctx):
        return await ctx.send('Please specify a category to add donations to.')

    # Giveaway
    @add_donations.command(name='giveaway')
    async def giveaway(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"giveaway": user_info["giveaway"] + amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 0))

    # Heist
    @add_donations.command(name='heist')
    async def heist(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"heist": user_info["heist"] + amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 1))

    # Event
    @add_donations.command(name='event')
    async def event(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"event": user_info["event"] + amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 2))

    # Special
    @add_donations.command(name='special')
    async def special(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"special": user_info["special"] + amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 3))

    # Money
    @add_donations.command(name='money')
    async def money(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"money": user_info["money"] + amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 4))

    '''
    Remove Donations
    '''
    @commands.group(name='remove_donations', description='Add donations to a user', aliases=['rd', 'dr'], invoke_without_command=True)
    async def remove_donations(self, ctx):
        return await ctx.send('Please specify a category to add donations to.')

    # Giveaway
    @remove_donations.command(name='giveaway', invoke_without_command=True)
    async def giveaway(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"giveaway": user_info["giveaway"] - amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 0))

    # Heist
    @remove_donations.command(name='heist', invoke_without_command=True)
    async def heist(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"heist": user_info["heist"] - amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 1))

    # Event
    @remove_donations.command(name='event', invoke_without_command=True)
    async def event(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"event": user_info["event"] - amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 2))

    # Special
    @remove_donations.command(name='special', invoke_without_command=True)
    async def special(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"special": user_info["special"] - amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 3))

    # Money
    @remove_donations.command(name='money', invoke_without_command=True)
    async def money(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        user_info = await self.get_user_amount(ctx, member)
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"money": user_info["money"] - amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 4))

    '''
    Set Donations
    '''
    @commands.group(name='set_donations', description='Add donations to a user', aiases=['sd', 'ds'], invoke_without_command=True)
    async def set_donations(self, ctx):
        return await ctx.send('Please specify a category to add donations to.')

    # Giveaway
    @set_donations.command(name='giveaway', invoke_without_command=True)
    async def giveaway(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"giveaway": amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 0))

    # Heist
    @set_donations.command(name='heist', invoke_without_command=True)
    async def heist(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"heist": amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 1))

    # Event
    @set_donations.command(name='event', invoke_without_command=True)
    async def event(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"event": amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 2))

    # Special
    @set_donations.command(name='special', invoke_without_command=True)
    async def special(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"special": amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 3))

    # Money
    @set_donations.command(name='money', invoke_without_command=True)
    async def money(self, ctx, member: discord.Member, amount: str):
        collection = self.db[str(ctx.guild.id)]
        amount = self.is_valid_int(amount)
        if not amount:
            return await ctx.send(f'`{amount}` is not a valid integer, please provide one that is valid')

        await collection.update_one({"_id": member.id}, {"$set": {f"money": amount}})

        await ctx.send(embed=self.embed(ctx, member, amount, 4))

def setup(bot):
    bot.add_cog(Testing(bot))