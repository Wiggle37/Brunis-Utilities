import discord
from discord.ext import commands

import sqlite3

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
    ADD TO DB/ADD ROLES
    '''
    #Get User
    def get_user(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        user = member.id
        amount = 0

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{member.id}'")
        result = cursor.fetchone()

        if result is None:

            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

            dbase.commit()
            dbase.close()

    #Auto Roles Self
    async def selfroles(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        member = ctx.author.id
        user = ctx.author

        cursor.execute(f"SELECT gaw FROM donations WHERE user_id = '{member}'")
        result1 = cursor.fetchone()
        result1 = (result1[0])

        cursor.execute(f"SELECT heist FROM donations WHERE user_id = '{member}'")
        result2 = cursor.fetchone()
        result2 = (result2[0])

        cursor.execute(f"SELECT event FROM donations WHERE user_id = '{member}'")
        result3 = cursor.fetchone()
        result3 = (result3[0])

        cursor.execute(f"SELECT money FROM donations WHERE user_id = '{member}'")
        result4 = cursor.fetchone()
        result4 = (result4[0])

        cursor.execute(f"SELECT special FROM donations WHERE user_id = '{member}'")
        result5 = cursor.fetchone()
        result5 = (result5[0])

        total = result1 + result2 + result3 + result4 + result5

        #5 Mil
        if total >= 5000000:
            role = discord.utils.find(lambda r: r.name == '✧ 5 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 5 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #10 Mil
        if total >= 10000000:
            role = discord.utils.find(lambda r: r.name == '✧ 10 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 10 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #25 Mil
        if total >= 25000000:
            role = discord.utils.find(lambda r: r.name == '✧ 25 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 25 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #50 Mil
        if total >= 50000000:
            role = discord.utils.find(lambda r: r.name == '✧ 50 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 50 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #100 Mil
        if total >= 100000000:
            role = discord.utils.find(lambda r: r.name == '✧ 100 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 100 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #250 Mil
        if total >= 250000000:
            role = discord.utils.find(lambda r: r.name == '✧ 250 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 250 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #500 Mil
        if total >= 500000000:
            role = discord.utils.find(lambda r: r.name == '✧ 500 million donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 500 million donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #1 Bil
        if total >= 1000000000:
            role = discord.utils.find(lambda r: r.name == '✧ 1 billion donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 1 billion donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        #2.5 Bil
        if total >= 2500000000:
            role = discord.utils.find(lambda r: r.name == '✧ 2.5 billion donor', ctx.message.guild.roles)
            if role in user.roles:
                pass
            
            else:
                role = discord.utils.get(ctx.guild.roles, name='✧ 2.5 billion donor')
                await user.add_roles(role)
                await ctx.send(f'You now have the `{role}` role! Tysm for donating!')

        dbase.commit()
        dbase.close()

    #Auto Roles Non-Self
    async def roles(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        member_id = member.id
        user = member

        cursor.execute(f"SELECT gaw FROM donations WHERE user_id = '{member_id}'")
        result1 = cursor.fetchone()
        result1 = (result1[0])

        cursor.execute(f"SELECT heist FROM donations WHERE user_id = '{member_id}'")
        result2 = cursor.fetchone()
        result2 = (result2[0])

        cursor.execute(f"SELECT event FROM donations WHERE user_id = '{member_id}'")
        result3 = cursor.fetchone()
        result3 = (result3[0])

        cursor.execute(f"SELECT money FROM donations WHERE user_id = '{member_id}'")
        result4 = cursor.fetchone()
        result4 = (result4[0])

        cursor.execute(f"SELECT special FROM donations WHERE user_id = '{member_id}'")
        result5 = cursor.fetchone()
        result5 = (result5[0])

        total = result1 + result2 + result3 + result4 + result5

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

    #Make Acc Command(Backup)
    @commands.command()
    async def init(self, ctx):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        user = ctx.author.id
        member = ctx.author
        amount = 0

        cursor.execute(f"SELECT user_id FROM donations WHERE user_id = '{member.id}'")
        result = cursor.fetchone()

        if result is None:

            cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

        else:
            await ctx.send('You are already in the database!')

    '''
    DONATIONS CHECK
    '''
    #Check Dono
    @commands.command(aliases=['d'])
    async def dono(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        
        #No Member Provided
        if member is None:
            await self.selfroles(ctx, member)

            #Get Gaw Amount
            cursor.execute(f"SELECT gaw FROM donations WHERE user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()

            #Get Heist Amount
            cursor.execute(f"SELECT heist FROM donations WHERE user_id = '{ctx.author.id}'")
            result2 = cursor.fetchone()

            #Get Event Amount
            cursor.execute(f"SELECT event FROM donations WHERE user_id = '{ctx.author.id}'")
            result3 = cursor.fetchone()

            #Get Money Amount
            cursor.execute(f"SELECT money FROM donations WHERE user_id = '{ctx.author.id}'")
            result4 = cursor.fetchone()

            #Get Special Event Amount
            cursor.execute(f"SELECT special FROM donations WHERE user_id = '{ctx.author.id}'")
            result5 = cursor.fetchone()

        #Member Provided
        else:
            await self.roles(ctx, member)

            #Get Gaw Amount
            cursor.execute(f"SELECT gaw FROM donations WHERE user_id = '{member.id}'")
            result1 = cursor.fetchone()

            #Get Heist Amount
            cursor.execute(f"SELECT heist FROM donations WHERE user_id = '{member.id}'")
            result2 = cursor.fetchone()

            #Get Event Amount
            cursor.execute(f"SELECT event FROM donations WHERE user_id = '{member.id}'")
            result3 = cursor.fetchone()

            #Get Money Amount
            cursor.execute(f"SELECT money FROM donations WHERE user_id = '{member.id}'")
            result4 = cursor.fetchone()

            #Get Special Event Amount
            cursor.execute(f"SELECT special FROM donations WHERE user_id = '{member.id}'")
            result5 = cursor.fetchone()

        result1 = (result1[0])
        new_result1 = ('{:,}'.format(result1))

        result2 = (result2[0])
        new_result2 = ('{:,}'.format(result2))

        result3 = (result3[0])
        new_result3 = ('{:,}'.format(result3))

        result4 = (result4[0])
        new_result4 = ('{:,}'.format(result4))

        result5 = (result5[0])
        new_result5 = ('{:,}'.format(result5))

        all = result1 + result2 + result3 + result5
        new_all = ('{:,}'.format(all))

        if member is None:
            embed = discord.Embed(title='Donation Stats', description=None, color=0x7008C2)

            embed.add_field(name='User:', value=f'{ctx.author.mention}(User id: {ctx.author.id})', inline=False)
            embed.add_field(name='__**Money Donations**__', value='Real Money Donations', inline=False)
            embed.add_field(name=f'Money Donations:', value=f'$`{new_result4}` donated in real money')

            embed.add_field(name='__**Normal Donations**__', value='Dank Memer Donations', inline=False)
            embed.add_field(name='Giveaway Donations:', value=f'⏣`{new_result1}` donated for giveaways', inline=False)
            embed.add_field(name='Heist Donations:', value=f'⏣`{new_result2}` donated for heists', inline=False)
            embed.add_field(name='Event Donations:', value=f'⏣`{new_result3}` donated for events', inline=False)
            embed.add_field(name='Special Event Donations:', value=f'⏣`{new_result5}`')

            embed.add_field(name='Total Donations:', value=f'⏣`{new_all}` donated in total', inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Donation Stats', description=None, color=0x7008C2)

            embed.add_field(name='User:', value=f'{member.mention}(User id: {member.id})', inline=False)
            embed.add_field(name='__**Money Donations**__', value='Real Money Donations', inline=False)
            embed.add_field(name=f'Money Donations:', value=f'$`{new_result4}` donated in real money')

            embed.add_field(name='__**Normal Donations**__', value='Dank Memer Donations', inline=False)
            embed.add_field(name='Giveaway Donations:', value=f'⏣`{new_result1}` donated for giveaways', inline=False)
            embed.add_field(name='Heist Donations:', value=f'⏣`{new_result2}` donated for heists', inline=False)
            embed.add_field(name='Event Donations:', value=f'⏣`{new_result3}` donated for events', inline=False)
            embed.add_field(name='Special Event Donations:', value=f'⏣`{new_result5}`')

            embed.add_field(name='Total Donations:', value=f'⏣`{new_all}` donated in total', inline=False)
            await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    @dono.error
    async def dono_error(self, ctx, error):
        await ctx.send('You are not in the database correctly. Use the command `b!init` to get added')

    '''
    MONEY DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['mds'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def money_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        reset = 0
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))
        
        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **${amount}**")

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
    async def money_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **${amount}**")

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
    async def money_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money - ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **${amount}**")

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
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money = ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **${amount}**")

        dbase.commit()
        dbase.close()

    @money_dono_reset.error
    async def money_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway managers can use this command')

    '''
    GIVEAWAY DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['gds'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        reset = 0
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

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
    async def gaw_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

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
    async def gaw_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw - ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

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
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw = ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

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
    async def heist_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        reset = 0
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

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
    async def heist_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

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
    async def heist_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist - ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

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
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist = ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

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
    async def event_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        reset = 0
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

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
    async def event_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

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
    async def event_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event - ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

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
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event = ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

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
    async def special_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        reset = 0
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount set was **⏣{amount}**")

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
    async def special_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **⏣{amount}**")

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
    async def special_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        self.get_user(ctx, member)
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special - ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        amount = ('{:,}'.format(amount))

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **⏣{amount}**")

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
        await self.roles(ctx, member)

        user = int(f'{member.id}')
        amount = 0

        cursor.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special = ?;", [user, amount, amount])

        message = ctx.message
        await message.add_reaction(emoji='<a:check~1:828448588488769588>')

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **⏣{amount}**")

        dbase.commit()
        dbase.close()

    @special_dono_reset.error
    async def special_event_dono_reset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('There are one or more required arguments that are missing')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permssion to do that\nOnly giveaway, heist, and event managers can use this command')

def setup(client):
    client.add_cog(Dono(client))