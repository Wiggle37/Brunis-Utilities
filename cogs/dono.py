import discord
from discord.ext import commands

import sqlite3

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Make Acc Command(Backup)
    @commands.command()
    async def init(self, ctx):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        user = ctx.author.id
        amount = 0

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO donations (user_id, total) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET total = total + ?;", [user, amount, amount])
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

    #Get User
    def get_user(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        user = member.id
        amount = 0

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{member.id}'")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO donations (user_id, total) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET total = total + ?;", [user, amount, amount])

        dbase.commit()
        dbase.close()

    #Auto Roles Non-Self
    async def roles(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        member_id = member.id
        user = member

        cursor.execute(f"SELECT total FROM donations WHERE user_id = '{member_id}'")
        total = cursor.fetchone()
        total = (total[0])

        #5 Mil
        if total >= 5000000:
            role = discord.utils.find(lambda r: r.name == '✧ 5 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 5 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #10 Mil
        if total >= 10000000:
            role = discord.utils.find(lambda r: r.name == '✧ 10 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 10 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #25 Mil
        if total >= 25000000:
            role = discord.utils.find(lambda r: r.name == '✧ 25 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 25 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #50 Mil
        if total >= 50000000:
            role = discord.utils.find(lambda r: r.name == '✧ 50 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 50 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #100 Mil
        if total >= 100000000:
            role = discord.utils.find(lambda r: r.name == '✧ 100 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 100 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #250 Mil
        if total >= 250000000:
            role = discord.utils.find(lambda r: r.name == '✧ 250 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 250 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #500 Mil
        if total >= 500000000:
            role = discord.utils.find(lambda r: r.name == '✧ 500 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 500 million donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #1 Bil
        if total >= 1000000000:
            role = discord.utils.find(lambda r: r.name == '✧ 1 billion donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 1 billion donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

        #2.5 Bil
        if total >= 2500000000:
            role = discord.utils.find(lambda r: r.name == '✧ 2.5 billion donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 2.5 billion donor')
                await user.add_roles(role)
                await ctx.send(f'**{member}** now has the `{role}` role! Tysm for donating!')

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

        cursor.execute(f"SELECT gaw, heist, event, special, total, money FROM donations WHERE user_id = '{user.id}'")
        gaw, heist, event, special, total, money = map(self.beautify_numbers, cursor.fetchone())

        donation_embed = discord.Embed(title="Donation Stats",color=0x7008C2)
        
        donation_embed.add_field(name="User:", value = f"{user.mention}(User id: {user.id})", inline=False)
        donation_embed.add_field(name="__**Money Donations**__", value="Money Donations", inline=False)
        donation_embed.add_field(name="Money Donations:", value = f"$`{money}` donated in real money")

        donation_embed.add_field(name="__**Normal Donations**__", value="Dank Memer Donations", inline=False)
        donation_embed.add_field(name="Giveaway Donations:", value = f"⏣`{gaw}` donated for giveaways", inline=False)
        donation_embed.add_field(name="Heist Donations:", value = f"⏣`{heist}` donated for heists", inline=False)
        donation_embed.add_field(name="Event Donations:", value = f"⏣`{event}` donated for events", inline=False)
        donation_embed.add_field(name="Special Event Donations:", value = f"⏣`{special}`", inline=False)

        donation_embed.add_field(name="Total Donations:", value = f"⏣`{total}` donated in total", inline=False)
        await ctx.send(embed=donation_embed)

    @dono.error
    async def dono_error(self, ctx, error):
        await ctx.send('You are not in the database correctly. Use the command `b!init` to get added')

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
            user = int(f'{member.id}')
            reset = 0

            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw = ?;", [user, reset, reset])
            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw - ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw = ?;", [user, amount, amount])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Giveaway\n**Amount Set:** 0\n\n**Updated by: {ctx.author}**', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')
            reset = 0

            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, reset, reset])
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist - ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, amount, amount])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Heist\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')
            reset = 0

            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, reset, reset])
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event - ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, amount, amount])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Event\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')
            reset = 0

            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, reset, reset])
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

            await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special - ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, amount, amount])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Special Event\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        await self.roles(ctx, member)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')
            reset = 0

            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, reset, reset])
            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount set was **${amount}**")

            await self.roles(ctx, member)

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Set:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')

            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note added for **{member}**\nThe amount added was **${amount}**")

            await self.roles(ctx, member)

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Added:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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
            user = int(f'{member.id}')
            amount = int(f'{amount}')

            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money - ?;", [user, amount, amount])

            cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

            message = ctx.message
            await message.add_reaction(emoji='<a:check~1:828448588488769588>')

            amount = ('{:,}'.format(amount))
            await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **${amount}**")

            embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Removed:** {amount}\n\n**Updated by:** {ctx.author}', color=0x00ff00)
            await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

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

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, amount, amount])

        cursor.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {user}")

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))
        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **${amount}**")

        embed = discord.Embed(title=f'Donations Updated For {member}', description=f'**Member:** {member}\n**Category:** Money\n**Amount Set:** 0\n\n**Updated by:** {ctx.author}', color=0x00ff00)
        await self.client.get_channel(838440247507288095).send(embed=embed)

        dbase.commit()
        dbase.close()

    @money_dono_reset.error
    async def money_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')
def setup(client):
    client.add_cog(Dono(client))