import discord
from discord.ext import commands

import sqlite3

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
    ADD TO DB/ADD ROLES
    '''
    #Make Acc
    @commands.command()
    async def init(self, ctx):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT user_id FROM special_event_dono_logs WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()

        if result is None:
            user = ctx.author.id
            amount = 0

            cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])
            cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

            await ctx.send('Added to database!')

            dbase.commit()
            dbase.close()

        else:
            await ctx.send('You are already in the database!')

    '''
    DONATIONS CHECK
    '''
    #Check Dono
    @commands.command(aliases=['d'])
    async def dono(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()
        
        #No Member Provided
        if member is None:
            #Get Gaw Amount
            cursor.execute(f"SELECT amount FROM gaw_dono_logs WHERE user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            if result1 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')
            #Get Heist Amount
            cursor.execute(f"SELECT amount FROM heist_dono_logs WHERE user_id = '{ctx.author.id}'")
            result2 = cursor.fetchone()
            if result2 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Event Amount
            cursor.execute(f"SELECT amount FROM event_dono_logs WHERE user_id = '{ctx.author.id}'")
            result3 = cursor.fetchone()
            if result3 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Money Amount
            cursor.execute(f"SELECT amount FROM money_dono_logs WHERE user_id = '{ctx.author.id}'")
            result4 = cursor.fetchone()
            if result4 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Special Event Amount
            cursor.execute(f"SELECT amount FROM special_event_dono_logs WHERE user_id = '{ctx.author.id}'")
            result5 = cursor.fetchone()
            if result5 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

        #Member Provided
        else:
            #Get Gaw Amount
            cursor.execute(f"SELECT amount FROM gaw_dono_logs WHERE user_id = '{member.id}'")
            result1 = cursor.fetchone()
            if result1 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')
            #Get Heist Amount
            cursor.execute(f"SELECT amount FROM heist_dono_logs WHERE user_id = '{member.id}'")
            result2 = cursor.fetchone()
            if result2 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Event Amount
            cursor.execute(f"SELECT amount FROM event_dono_logs WHERE user_id = '{member.id}'")
            result3 = cursor.fetchone()
            if result3 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Money Amount
            cursor.execute(f"SELECT amount FROM money_dono_logs WHERE user_id = '{member.id}'")
            result4 = cursor.fetchone()
            if result4 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

            #Get Special Event Amount
            cursor.execute(f"SELECT amount FROM special_event_dono_logs WHERE user_id = '{member.id}'")
            result5 = cursor.fetchone()
            if result5 is None:
                await ctx.send('Hmm there was an error\nThis ocurred because you are not in the database properly, pls use command `b!init` and if that doesnt work dm **<@765322777329664089>** for assistance')

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

    '''
    MONEY DONATIONS
    '''
    #Dono Set
    @commands.command(aliases=['mds'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def money_dono_set(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        reset = 0

        amount = int(f'{amount}')

        cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO money_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        reset = 0

        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO gaw_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        reset = 0

        amount = int(f'{amount}')

        cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO heist_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        reset = 0

        amount = int(f'{amount}')

        cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        reset = 0

        amount = int(f'{amount}')

        cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, reset, reset])

        cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [user, amount, amount])

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
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO special_event_dono_logs (user_id, amount) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [user, amount, amount])

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