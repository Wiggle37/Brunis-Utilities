import discord
from discord.ext import commands
import sqlite3
from functools import total_ordering
from os import curdir
from discord.utils import to_json

'''
General Donation Commands:
--- Commands for the general public for donations ---

| Command |     | Permissions |     | Description |
- b!dono    --- [             ] --- Check how much you or someone else has donated
- b!top     --- [             ] --- Check the top donators for the server in DMC and real money
- b!init    --- [             ] --- If you are not added into the database add yourself and yourself only into he database

Donations Management Commands:
--- Bruni and Bot Dev bypass all requirements for below commands ---

| Command |      | Permissions |
- b!gda      --- [             ]
- b!gdr      --- [             ]
- b!gds      --- [             ]
- b!gdrs     --- [             ]

- b!hda      --- [             ]
- b!hdr      --- [             ]
- b!hds      --- [             ]
- b!hdrs     --- [             ]

- b!eda      --- [             ]
- b!edr      --- [             ]
- b!eds      --- [             ]
- b!edrs     --- [             ]

- b!sda      --- [             ]
- b!sdr      --- [             ]
- b!sds      --- [             ]
- b!sdrs     --- [             ]

- b!mda      --- [             ]
- b!mdr      --- [             ]
- b!mds      --- [             ]
- b!mdrs     --- [             ]
'''

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
        return amount

        dbase.close()

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
    DONATIONS CHECK
    '''
    #Check Dono
    @commands.command(aliases=['d'])
    async def dono(self, ctx, member: discord.Member=None):
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

    @dono.error
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
    @commands.command(aliases=['gds'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_set(self, ctx, member: discord.Member, amount: str=None):
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @gaw_dono_set.error
    async def gaw_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Add
    @commands.command(aliases=['gda'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @gaw_dono_add.error
    async def gaw_dono_add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Remove
    @commands.command(aliases=['gdr'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @gaw_dono_remove.error
    async def gaw_dono_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Reset
    @commands.command(aliases=['gdrs'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Set:** 0\n\n**Updated by: {ctx.author}**', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @gaw_dono_reset.error
    async def gaw_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    '''
    HEIST DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['hds'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThe have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @heist_dono_set.error
    async def heist_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Add
    @commands.command(aliases=['hda'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manger, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @heist_dono_add.error
    async def heist_dono_add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly heist managers can use this command')

    #Dono Remove
    @commands.command(aliases=['hdr'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manger, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @heist_dono_remove.error
    async def heist_dono_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly heist managers can use this command')

    #Dono Reset
    @commands.command(aliases=['hdrs'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manger, Bruni, Bot Dev
    async def heist_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = int(f'{member.id}')

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, 0, 0])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @heist_dono_reset.error
    async def heist_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly heist managers can use this command')

    '''
    EVENT DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['eds'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(amount)}")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @event_dono_set.error
    async def event_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly event managers can use this command')

    #Dono Add
    @commands.command(aliases=['eda'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()

        await self.roles(ctx, member)

    @event_dono_add.error
    async def event_dono_add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly event managers can use this command')

    #Dono Remove
    @commands.command(aliases=['edr'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()

        await self.roles(ctx, member)

    @event_dono_remove.error
    async def event_dono_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly event managers can use this command')

    #Dono Reset
    @commands.command(aliases=['edrs'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
    async def event_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @event_dono_reset.error
    async def event_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly event managers can use this command')

    '''
    SPECIAL EVENT
    '''
    #Dono Set
    @commands.command(aliases=['sds'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @special_dono_set.error
    async def special_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway, heist, and event managers can use this command')

    #Giveaway Dono Add
    @commands.command(aliases=['sda'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @special_dono_add.error
    async def special_event_dono_add_remove(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway, heist, and event managers can use this command')

    #Dono Remove
    @commands.command(aliases=['sdr'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev
    async def special_dono_remove(self, ctx, member: discord.Member, amount: int=None):
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            total = self.get_amount(ctx, member)
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{'{:,}'.format(amount)}**\nThey have now donated a total of **{'{:,}'.format(total)}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @special_dono_remove.error
    async def special_event_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway, heist, and event managers can use this command')

    #Dono Reset
    @commands.command(aliases=['sdrs'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 791516116710064159, 785202756641619999, 788738308879941633) #Giveaway Manager, Heist Manager, Event Manager, Bruni, Bot Dev
    async def special_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣0**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()

        await self.roles(ctx, member)

    @special_dono_reset.error
    async def special_event_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway, heist, and event managers can use this command')
    '''
    MONEY DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['mds'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **${amount}**")

            await self.roles(ctx, member)

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @money_dono_set.error
    async def money_dono_set_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Add
    @commands.command(aliases=['mda'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **${amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @money_dono_add.error
    async def money_dono_add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Remove
    @commands.command(aliases=['mdr'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
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
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            dbase.commit()

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **${amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @money_dono_remove.error
    async def money_dono_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    #Dono Reset
    @commands.command(aliases=['mdrs'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def money_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        self.get_user(ctx, member)
        user = member.id

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, 0, 0])
        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        dbase.commit()

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **$0**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.close()
        await self.roles(ctx, member)

    @money_dono_reset.error
    async def money_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')
            
def setup(client):
    client.add_cog(Dono(client))
