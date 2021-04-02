import discord
from discord.ext import commands
import sqlite3

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client


    '''
    ADD TO DATABASE
    '''
    @commands.Cog.listener()
    async def on_message(self, ctx):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        user = f'{ctx.author.id}'
        guild = f'{ctx.guild.id}'

        cursor.execute(f"SELECT user_id FROM gaw_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{ctx.author.id}'")
        result = cursor.fetchone()

        if result is None:
            amount = 0
            cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO heist_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            print(f'Member added to database\nUSER: {ctx.author}\nID: {ctx.author.id}')

        else:
            pass

        dbase.commit()
        dbase.close()

    '''
    DONATIONS CHECK
    '''
    @commands.command(aliases=['d'])
    async def dono(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        #Get Gaw Amount
        cursor.execute(f"SELECT amount FROM gaw_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result1 = cursor.fetchone()
        if result1 is None:
            await ctx.send('Donate to giveaways')

        #Get Heist Amount
        cursor.execute(f"SELECT amount FROM heist_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result2 = cursor.fetchone()
        if result2 is None:
            await ctx.send("Donate to heists")

        #Get Event Amount
        cursor.execute(f"SELECT amount FROM event_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result3 = cursor.fetchone()
        if result3 is None:
            await ctx.send('Donate to events')

        result1 = (result1[0])
        new_result1 = ('{:,}'.format(result1))

        result2 = (result2[0])
        new_result2 = ('{:,}'.format(result2))

        result3 = (result3[0])
        new_result3 = ('{:,}'.format(result3))


        all = result1 + result2 + result3
        new_all = ('{:,}'.format(all))

        embed = discord.Embed(title='Donation Stats', description=None, color=0x00ff00)
        embed.add_field(name='User:', value=f'{member.mention}(User id: {member.id})', inline=False)
        embed.add_field(name='Giveaway Donations:', value=f'`{new_result1}` donated for giveaways in **{ctx.guild.name}**', inline=False)
        embed.add_field(name='Heist Donations:', value=f'`{new_result2}` donated for heists in **{ctx.guild.name}**', inline=False)
        embed.add_field(name='Event Donations:', value=f'`{new_result3}` donated for events in **{ctx.guild.name}**', inline=False)
        embed.add_field(name='Total Donations:', value=f'`{new_all}` donated in total for **{ctx.guild.name}**', inline=False)
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    '''
    GIVEAWAY DONATIONS
    '''
    #Giveaway Dono Add
    @commands.command(aliases=['gda'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['gdr'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Reset
    @commands.command(aliases=['gdrs'])
    @commands.has_any_role(785198646731604008, 785202756641619999, 788738308879941633) #Giveaway Manager, Bruni, Bot Dev
    async def gaw_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **{amount}**")

        dbase.commit()
        dbase.close()

    '''
    HEIST DONATIONS
    '''
    #Dono Add
    @commands.command(aliases=['hda'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manger, Bruni, Bot Dev
    async def heist_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO heist_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['hdr'])
    @commands.has_any_role(785631914010214410, 785202756641619999, 788738308879941633) #Heist Manger, Bruni, Bot Dev
    async def heist_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO heist_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Reset
    @commands.command(aliases=['hdrs'])
    @commands.has_any_role(785631914010214410, 785202756641619999) #Heist Manger, Bruni
    async def heist_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO heist_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **{amount}**")

        dbase.commit()
        dbase.close()

    '''
    EVENT DONATIONS
    '''
    #Giveaway Dono Add
    @commands.command(aliases=['eda'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
    async def event_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['edr'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
    async def event_dono_remove(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Reset
    @commands.command(aliases=['edrs'])
    @commands.has_any_role(791516116710064159, 785202756641619999, 788738308879941633) #Event Manger, Bruni, Bot Dev
    async def event_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **{amount}**")

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Dono(client))