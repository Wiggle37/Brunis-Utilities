import discord
from discord.ext import commands

import aiosqlite
import aiohttp
from datetime import datetime
import asyncio

from config import *
from donofuncs import *
from buttons import *

class Dono(commands.Cog, name='donations', description='Tracks the servers donations by person'):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.dank_merchants = self.bot.get_guild(CONFIG["info"]["ids"]["merchants_id"])

    #Make Acc Command(Backup)
    @commands.command(hidden=True)
    async def init(self, ctx):
        dbase = await aiosqlite.connect('dono.db')
        cursor = await dbase.cursor()
        user = ctx.author.id

        await cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{ctx.author.id}'")
        result = await cursor.fetchone()

        if result is None:
            await cursor.execute("INSERT INTO donations (user_id, total) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET total = total + ?;", [user, 0, 0])
            await ctx.send('Added to database!')

        else:
            await ctx.send('You are already in the database!')

        await dbase.commit()
        await dbase.close()

    '''
    Functions
    '''
    #Abuse Check
    async def aboose(self, ctx, person, amount):
        if person == ctx.author:
            embed = discord.Embed(title=f'**Warning, {ctx.author} has updated their own donations**', description=f'Please keep an eye on this person they are mad sus\n**More Info:**\nUser: {ctx.author}({ctx.author.id})\nChannel: {ctx.channel.mention}\nAmount: {"{:,}".format(amount)}', color=0xff0000)
            await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Number Converter
    def is_valid_int(self, amount):
        try:
            float(amount.replace("m","").replace("k",""))
            return int(eval(amount.replace("k","e3").replace("m", "e6")))
            
        except ValueError:
            return False

    #Get User
    async def get_member(self, ctx, member: discord.Member=None):
        dbase = await aiosqlite.connect('dono.db')
        cursor = await dbase.cursor()
        user = member or ctx.author

        await cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{user.id}'")
        result = await cursor.fetchone()

        if result is None:
            await cursor.execute("INSERT INTO donations (user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET user_id = ?;", [user.id, user.id])

        await dbase.commit()
        await dbase.close()

    #Get Amount
    async def get_amount(self, ctx, member: discord.Member):
        dbase = await aiosqlite.connect('dono.db')
        cursor = await dbase.cursor()
        await self.get_member(ctx, member)

        member = member or ctx.author

        await cursor.execute(f"SELECT total FROM donations WHERE user_id = '{member.id}'")
        amount = await cursor.fetchone()
        await dbase.close()
        return amount[0]

    async def roles(self, ctx, user: discord.Member):
        user_roles_id = [role.id for role in user.roles]

        total = await self.get_amount(ctx, user)

        donors_roles = {
            5000000: 787342154862166046, # 5 million
            10000000: 787342156573704203, # 10 million
            25000000: 799022090791419954, # 25 million
            50000000: 787868761528336427, # 50 million
            100000000: 787868759720722493, # 100 million
            250000000: 799844364389187616, # 250 million
            500000000: 799022083778543696, # 500 million
            1000000000: 799844367551692827, # 1 billion
            2500000000: 824615522934849607, # 2.5 billion
            5000000000: 786610853033541632 # 5 billion
        }

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

    #Beatify Numbers
    def beautify_numbers(self, num):
        return "{:,}".format(num)

    '''
    Owner Commands
    '''
    #Reset Special
    @commands.command(name='endspecial', description='End the special leaderboard', hidden=True)
    @commands.is_owner()
    async def endspecial(self, ctx):
        async with ctx.typing():
            view = Confirm()
            await ctx.send('Are you sure you want to continue? This is remove all special donations and convert them into normal donations.', view=view)
            await view.wait()
            if view.value is None:
                await ctx.send('Confirmation timed out...')

            elif view.value:
                dbase = await aiosqlite.connect('dono.db')
                cursor = await dbase.cursor()

                await cursor.execute(f"SELECT user_id, special FROM donations")
                users = cursor.fetchall()

                for user in users:
                    await cursor.execute(f"UPDATE donations SET special = 0 WHERE user_id = '{int(user[0])}'")
                    await cursor.execute(f"UPDATE donations SET event = '{int(user[1])}' + event WHERE user_id = '{user[0]}'")

                    person = await self.bot.fetch_user(user[0])
                    await ctx.send(f"{person.name}'s special donations were reset to **0** and added {user[1]} to events")

                await ctx.send('All done coverting special donations into normal donations and ready to go for the next big event')

                await dbase.commit()
                await dbase.close()
            
            elif not view.value:
                await ctx.send('Ok cancelled')

    #Prune Database
    @commands.command(name='prunedb', description='Delete old users from the database that aren\'t in the server anymore', hidden=True)
    @commands.is_owner()
    async def prunedb(self, ctx):
        async with ctx.typing():
            view = Confirm()
            await ctx.send('Are you sure you want to clear the datebase of all members that have left Dank Merchants?', view=view)
            await view.wait()
            if view.value is None:
                await ctx.send('Confirmation timed out...')

            if view.value:
                dbase = await aiosqlite.connect('dono.db')
                cursor = await dbase.cursor()

                await cursor.execute(f"SELECT user_id FROM donations")
                results = await cursor.fetchall()

                num = 0

                for user in results:
                    member = self.dank_merchants.get_member(user[0])
                    if member is None:
                        num += 1
                        await cursor.execute(f"DELETE FROM donations WHERE user_id = '{user[0]}'")
                        print(f'{user[0]} was deleted from the db')
                        await ctx.send(f'{user[0]} deleted from database')

                        await asyncio.sleep(2.5)

                    else:
                        pass

                await dbase.commit()
                await dbase.close()

                await ctx.send(f'Done pruning members from the database that have left the server, {num} people were removed')

            elif not view.value:
                await ctx.send('Ok cancelled')

    '''
    DONATIONS CHECK
    '''
    #Check Dono
    @commands.command(name='donations', description='Check yours or someone elses donations', aliases=['d', 'dono', 'donation'])
    async def donations(self, ctx, member: discord.Member=None):
        dbase = await aiosqlite.connect("dono.db")
        cursor = await dbase.cursor()
        user = member or ctx.author

        await self.get_member(ctx, user)

        await cursor.execute(f"SELECT gaw, heist, event, special, total, money FROM donations WHERE user_id = '{user.id}'")
        gaw, heist, event, special, total, money = map(self.beautify_numbers, await cursor.fetchone())

        donation_embed = discord.Embed(title="Donation Stats", color=0x7008C2)
        donation_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/827369094776356905/828079209623584818/dankmerchants.gif')
        donation_embed.add_field(name="User:", value = f"{user.mention}(User id: {user.id})", inline=False)
        donation_embed.add_field(name="__**✦ Normal Donations ✦**__", value="Dank Memer Donations", inline=False)
        donation_embed.add_field(name="Giveaway Donations:", value = f"⏣`{gaw}` donated for giveaways", inline=True)
        donation_embed.add_field(name="Heist Donations:", value = f"⏣`{heist}` donated for heists", inline=True)
        donation_embed.add_field(name="Event Donations:", value = f"⏣`{event}` donated for events", inline=True)
        donation_embed.add_field(name="__**✦ Special Donations ✦**__", value="Money Donations", inline=False)
        donation_embed.add_field(name="Special Event Donations:", value = f"⏣`{special}`", inline=True)
        donation_embed.add_field(name="Money Donations:", value = f"$`{money}` donated in real money", inline=True)
        donation_embed.add_field(name="__**Total Donations:**__", value = f"⏣`{total}` donated in total", inline=False)
        await ctx.send(embed=donation_embed)

        await dbase.close()

    #Tops
    @commands.command(name='top', description='Check the leaderboard of the top donations', aliases=['tops'])
    async def top(self, ctx, board='donor'):
        if board.lower() == 'donor' or board.lower() == 'dank' or board.lower() == 'donors' or board.lower() == 'total':
            dbase = await aiosqlite.connect("dono.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, total FROM donations ORDER BY total DESC")
            dank_donors = await cursor.fetchmany(25)

            top_donors_embed = discord.Embed(title="Top Total donors!", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Dank Memer Donations Leader Board**__\n"
            for rank, user in enumerate(dank_donors):
                member = self.bot.get_user(user[0])
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            await dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'money' or board.lower() == 'moneys':
            dbase = await aiosqlite.connect("dono.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, money FROM donations ORDER BY money DESC")
            money_donors = await cursor.fetchmany(5)

            top_donors_embed = discord.Embed(title="Top Money Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Real Money Donations Leader Board**__\n"
            for rank, user in enumerate(money_donors):
                member = self.bot.get_user(user[0])
                donor_info += f"**{rank + 1}. {member}**: `${'{:,}'.format(user[1])} USD`\n"

            top_donors_embed.description=donor_info
            await dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'bumps' or board.lower() == 'bump':
            dbase = await aiosqlite.connect("bump.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, bump FROM bumps ORDER BY bump DESC")
            bumpers = await cursor.fetchmany(10)

            top_bumpers_embed = discord.Embed(title="Top Bumpers", color=0x00ff00)
            bumper_info = ""

            bumper_info += "__**Server Bumps Leader board**__\n"
            for rank, user in enumerate(bumpers):
                member = self.bot.get_user(user[0])
                bumper_info += f"**{rank + 1}. {member}**: `{'{:,}'.format(user[1])}`\n"
            
            top_bumpers_embed.description=bumper_info
            await dbase.close()
            
            return await ctx.send(embed=top_bumpers_embed)
        
        if board.lower() == 'special':
            dbase = await aiosqlite.connect("dono.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, special FROM donations ORDER BY special DESC")
            special_donors = await cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Special Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Special Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = self.bot.get_user(user[0])
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            await dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'heist':
            dbase = await aiosqlite.connect("dono.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, heist FROM donations ORDER BY heist DESC")
            special_donors = await cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Heist Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Heist Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = self.bot.get_user(user[0])
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            await dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'event':
            dbase = await aiosqlite.connect("dono.db")
            cursor = await dbase.cursor()

            await cursor.execute("SELECT user_id, event FROM donations ORDER BY event DESC")
            special_donors = await cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Event Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Event Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = self.bot.get_user(user[0])
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            await dbase.close()
            return await ctx.send(embed=top_donors_embed)

    '''
    GIVEAWAY DONATIONS
    '''
    #Dono Set
    @commands.command(name='gds', description='Set someones giveaway donations')
    @commands.has_any_role(785198646731604008, 784492058756251669, 788738305365114880) # Giveaway Manager, Admin, Co-Owner
    async def gaw_dono_set(self, ctx, member: discord.Member, amount: str):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.set(ctx, 'gaw', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='gda', description='Add to someones giveaway donations')
    @commands.has_any_role(785198646731604008, 784492058756251669, 788738305365114880) # Giveaway Manager, Admin, Co-Owner
    async def gaw_dono_add(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.add(ctx, 'gaw', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='gdr', description='Remove from someones giveaway donations')
    @commands.has_any_role(785198646731604008, 784492058756251669, 788738305365114880) # Giveaway Manager, Admin, Co-Owner
    async def gaw_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.remove(ctx, 'gaw', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='gdrs', description='Reset someones giveaway donations')
    @commands.has_any_role(785198646731604008, 784492058756251669, 788738305365114880) # Giveaway Manager, Admin, Co-Owner
    async def gaw_dono_reset(self, ctx, member: discord.Member):
        await self.get_member(ctx, member)

        await dono.reset(ctx, 'gaw', member)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, 0)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    '''
    HEIST DONATIONS
    '''
    #Dono Set
    @commands.command(name='hds', description='Set someones heist donations')
    @commands.has_any_role(785631914010214410, 784492058756251669, 788738305365114880) # Heist Manager, Admin, Co-Owner
    async def heist_dono_set(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.set(ctx, 'heist', member, amount)
        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThe have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='hda', description='Add to someones heist donations')
    @commands.has_any_role(785631914010214410, 784492058756251669, 788738305365114880) # Heist Manger, Admin, Co-Owner
    async def heist_dono_add(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        total = await dono.add(ctx, 'heist', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='hdr', description='Remove from someones heist donations')
    @commands.has_any_role(785631914010214410, 784492058756251669, 788738305365114880) # Heist Manger Admin, Co-Owner
    async def heist_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.remove(ctx, 'heist', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        total = await self.get_amount(ctx, member)
        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='hdrs', description='Reset someones heist donations')
    @commands.has_any_role(785631914010214410, 784492058756251669, 788738305365114880) # Heist Manger, Admin, Co-Owner
    async def heist_dono_reset(self, ctx, member: discord.Member):
        await self.get_member(ctx, member)

        await dono.reset(ctx, 'heist', member)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, 0)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    '''
    EVENT DONATIONS
    '''
    #Dono Set
    @commands.command(name='eds', description='Set someones event donations')
    @commands.has_any_role(791516116710064159, 784492058756251669, 788738305365114880) # Event Manager, Admin, Co-Owner
    async def event_dono_set(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')
        
        total = await dono.set(ctx, 'event', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='eda', description='Add to someones event donations')
    @commands.has_any_role(791516116710064159, 784492058756251669, 788738305365114880) # Event Manger, Admin, Co-Owner
    async def event_dono_add(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.add(ctx, 'event', member, amount)
        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='edr', description='Remove from someones event donations')
    @commands.has_any_role(791516116710064159, 784492058756251669, 788738305365114880) # Event Manger, Admin, Co-Owner
    async def event_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.remove(ctx, 'event', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='edrs', description='Reset someones event donations')
    @commands.has_any_role(791516116710064159, 784492058756251669, 788738305365114880) # Event Manger, Admin, Co-Owner
    async def event_dono_reset(self, ctx, member: discord.Member):
        await self.get_member(ctx, member)

        await dono.reset(ctx, 'event', member)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, 0)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    '''
    SPECIAL EVENT
    '''
    #Dono Set
    @commands.command(name='sds', description='Set someones special donations')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 784527745539375164, 784492058756251669, 788738305365114880) # Giveaway Manager, Heist Manager, Event Manager, Mod, Admin, Co-Owner
    async def special_dono_set(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.set(ctx, 'special', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='sda', description='Add to someones special donations')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 784527745539375164, 784492058756251669, 788738305365114880) # Giveaway Manager, Heist Manager, Event Manager, Admin, Co-Owner
    async def special_dono_add(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.add(ctx, 'special', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='sdr', description='Remove from someones special donations')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 784527745539375164, 784492058756251669, 788738305365114880) # Giveaway Manager, Heist Manager, Event Manager, Mod, Admin, Co-Owner
    async def special_dono_remove(self, ctx, member: discord.Member, amount: str):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        total = await dono.remove(ctx, 'special', member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, amount)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='sdrs', description='Reset someones special donations')
    @commands.has_any_role(784492058756251669, 788738305365114880) # Admin, Co-Owner
    async def special_dono_reset(self, ctx, member: discord.Member):
        await self.get_member(ctx, member)

        await dono.reset(ctx, 'special', member)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        await self.roles(ctx, member)
        await self.aboose(ctx, member, 0)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    '''
    MONEY DONATIONS
    '''
    #Dono Set
    @commands.command(name='mds', description='Set someones money donations')
    @commands.has_any_role(788738305365114880, 788738308879941633) #Co-Owner, Bot Dev
    async def money_dono_set(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')
        
        await money.set(member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **${amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount set: `⏣{amount}`', color=0x00ff00)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='mda', description='Add to someones money donations')
    @commands.has_any_role(788738305365114880, 788738308879941633) #Co-Owner, Bot Dev
    async def money_dono_add(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        await money.add(member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **${amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount added: `⏣{amount}`', color=0x00ff00)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='mdr', description='Remove from someones money donations')
    @commands.has_any_role(788738305365114880, 785202756641619999, 788738308879941633) #Co-Owner, Bruni, Bot Dev
    async def money_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        await self.get_member(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            return await ctx.send('Not a valid number there bud')

        await money.remove(member, amount)

        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **${amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount removed: `⏣{amount}`', color=0xff0000)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='mdrs', description='Reset someones money donations')
    @commands.has_any_role(788738305365114880, 788738308879941633) #Co-Owner, Bot Dev
    async def money_dono_reset(self, ctx, member: discord.Member):
        await self.get_member(ctx, member)

        await money.reset(member)
        
        await ctx.message.add_reaction(emoji='<a:greencheck:853007357709910086>')
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **$0**")

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\n**AMOUNT RESET TO 0**', color=0xff0000)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.bot.get_channel(854363438616936498).send(embed=embed)
            
def setup(bot):
    bot.add_cog(Dono(bot))