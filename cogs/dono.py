import discord
from discord.ext import commands
import sqlite3
import datetime
from datetime import datetime

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Make Acc Command(Backup)
    @commands.command()
    async def init(self, ctx):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        user = ctx.author.id

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO donations (user_id, total) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET total = total + ?;", [user, 0, 0])
            await ctx.send('Added to database!')

        else:
            await ctx.send('You are already in the database!')

        dbase.commit()
        dbase.close()

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

    #Get Amount
    def get_amount(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        member = (member or ctx.author).id

        cursor.execute(f"SELECT total FROM donations WHERE user_id = '{member}'")
        amount = cursor.fetchone()[0]
        dbase.close()
        return amount

    #Get User
    def get_user(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        user = (member or ctx.author).id

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{user}'")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO donations (user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET user_id = ?;", [user, user])

        dbase.commit()
        dbase.close()

    async def roles(self, ctx, user: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        user_roles_id = [role.id for role in user.roles]

        cursor.execute(f"SELECT total FROM donations WHERE user_id = '{user.id}'")
        total = cursor.fetchone()[0]

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
    BRUNI ONY LOL(well ig bot owners...)
    '''
    @commands.command()
    @commands.is_owner()
    async def endspecial(self, ctx):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT user_id, special FROM donations")
        users = cursor.fetchall()

        for user in users:
            cursor.execute(f"UPDATE donations SET special = 0 WHERE user_id = '{int(user[0])}'")
            cursor.execute(f"UPDATE donations SET event = '{int(user[1])}' + event WHERE user_id = '{user[0]}'")

            person = await self.client.fetch_user(user[0])
            await ctx.send(f"{person.name}'s special donations were reset to **0** and added {user[1]} to events")

        await ctx.send('ALL DONE!!')

        dbase.commit()
        dbase.close()

    '''
    DONATIONS CHECK
    '''
    #Check Dono
    @commands.command(aliases=['d', 'dono', 'donation'])
    async def donations(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect("dono.db")
        cursor = dbase.cursor()
        user = member or ctx.author

        self.get_user(ctx, user)

        cursor.execute(f"SELECT gaw, heist, event, special, total, money FROM donations WHERE user_id = '{user.id}'")
        gaw, heist, event, special, total, money = map(self.beautify_numbers, cursor.fetchone())

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

        dbase.close()

    @donations.error
    async def dono_error(self, ctx, error):
        if error == "Command raised an exception: TypeError: 'NoneType' object is not iterable":
            await ctx.send('Use the command `b!init` to be added to the db, sorry for the error')

        else:
            await ctx.send(f'There was an error\nError: `{error}`\nPlease dm Wiggle so he can fix it')

    #Top Donators
    @commands.command()
    async def top(self, ctx):
        dbase = sqlite3.connect("dono.db")
        cursor = dbase.cursor()

        cursor.execute("SELECT user_id, total FROM donations ORDER BY total DESC")
        dank_donors = cursor.fetchmany(5)

        top_donors_embed = discord.Embed(title="Top donors!", color=0x00ff00)

        donor_info = ""

        donor_info += "__**Dank memer donations**__\n"
        dank_merchants = self.client.get_guild(784491141022220309)
        for rank, user in enumerate(dank_donors):
            member = dank_merchants.get_member(int(user[0]))
            donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

        cursor.execute("SELECT user_id, money FROM donations ORDER BY money DESC")
        money_donors = cursor.fetchmany(3)

        donor_info += "__**Real Money Donations**__\n"
        for rank, user in enumerate(money_donors):
            member = ctx.guild.get_member(int(user[0]))
            donor_info += f"**{rank + 1}. {member}**: `${'{:,}'.format(user[1])}`\n"

        top_donors_embed.description=donor_info
        await ctx.send(embed=top_donors_embed)

        dbase.close()

    '''
    GIVEAWAY DONATIONS
    '''
    #Dono Set
    @commands.command(name='gds')
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def gaw_dono_set(self, ctx, member: discord.Member, amount: str):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='gda')
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def gaw_dono_add(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='gdr')
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def gaw_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw - ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='gdrs')
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def gaw_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Giveaway`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    '''
    HEIST DONATIONS
    '''
    #Dono Set
    @commands.command(name='hds')
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Heist Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def heist_dono_set(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThe have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='hda')
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Heist Manger, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def heist_dono_add(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='hdr')
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Heist Manger, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def heist_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist - ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='hdrs')
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Heist Manger, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def heist_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = int(f'{member.id}')

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, 0, 0])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Heist`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    '''
    EVENT DONATIONS
    '''
    #Dono Set
    @commands.command(name='eds')
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Event Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def event_dono_set(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)

        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(amount)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='eda')
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Event Manger, Bruni, Bot Dev, Mod Admin, Co-Owner
    async def event_dono_add(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='edr')
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Event Manger, Bruni, Bot Dev, Modr Admin, Co-Owner
    async def event_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event - ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='edrs')
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Event Manger, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def event_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Event`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    '''
    SPECIAL EVENT
    '''
    #Dono Set
    @commands.command(name='sds')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def special_dono_set(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount set: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='sda')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def special_dono_add(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount added: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='sdr')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def special_dono_remove(self, ctx, member: discord.Member, amount: str):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special - ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\nAmount removed: `⏣{self.beautify_numbers(amount)}`')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='sdrs')
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633, 784527745539375164, 784492058756251669, 788738305365114880) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev, Mod, Admin, Co-Owner
    async def special_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Special`\n**AMOUNT RESET TO 0**')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    '''
    MONEY DONATIONS
    '''
    #Dono Set
    @commands.command(name='mds')
    @commands.has_any_role(788738305365114880, 785202756641619999, 788738308879941633) #Co-Owner, Bruni, Bot Dev
    async def money_dono_set(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id

            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **${amount}**")

            await self.roles(ctx, member)

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount set: `⏣{amount}`', color=0x00ff00)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Add
    @commands.command(name='mda')
    @commands.has_any_role(788738305365114880, 785202756641619999, 788738308879941633) #Co-Owner, Bruni, Bot Dev
    async def money_dono_add(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id

            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **${amount}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount added: `⏣{amount}`', color=0x00ff00)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Remove
    @commands.command(name='mdr')
    @commands.has_any_role(788738305365114880, 785202756641619999, 788738308879941633) #Co-Owner, Bruni, Bot Dev
    async def money_dono_remove(self, ctx, member: discord.Member, amount: str=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        amount = self.is_valid_int(amount)
        if amount == False:
            await ctx.send('Not a valid number there bud')

        else:
            user = member.id
            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money - ?;", [user, amount, amount])
            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **${amount}**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\nAmount removed: `⏣{amount}`', color=0xff0000)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)

    #Dono Reset
    @commands.command(name='mdrs')
    @commands.has_any_role(788738305365114880, 785202756641619999, 788738308879941633) #Co-Owner, Bruni, Bot Dev
    async def money_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:greencheck:853007357709910086>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **$0**")

        dbase.close()
        await self.roles(ctx, member)

        embed = discord.Embed(title=f'Donations Updated For {member.display_name}', description=f'Category: `Money`\n**AMOUNT RESET TO 0**', color=0xff0000)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'Manager: {ctx.author}', icon_url='https://cdn.discordapp.com/emojis/851599382633250856.png?v=1')
        await self.client.get_channel(854363438616936498).send(embed=embed)
            
def setup(client):
    client.add_cog(Dono(client))