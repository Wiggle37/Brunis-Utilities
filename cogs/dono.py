import discord
from discord.ext import commands
import sqlite3

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        num = 10000000
        await ctx.send(f"{num:,}")

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

        
        num = f'{result1[0]}'
        print(f'{num:,}')

        #Get Heist Amount
        cursor.execute(f"SELECT amount FROM gaw_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result2 = cursor.fetchone()

        #Get Event Amount
        cursor.execute(f"SELECT amount FROM gaw_dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result3 = cursor.fetchone()

        embed = discord.Embed(title='Donation Stats', description=None, color=0x00ff00)
        embed.add_field(name='User:', value=f'{member.mention}(User id: {member.id})', inline=False)
        embed.add_field(name='Giveaway Donations:', value=f'`{result1[0]}` donated for giveaways in **{ctx.guild.name}**', inline=False)
        embed.add_field(name='Heist Donations:', value=f'`Coming Soon...` donated for heists in **{ctx.guild.name}**', inline=False)
        embed.add_field(name='Event Donations:', value=f'`Coming Soon...` donated for events in **{ctx.guild.name}**')
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    '''
    GIVEAWAY DONATIONS
    '''
    #Giveaway Dono Add
    @commands.command(aliases=['gda'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def gaw_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['gdr'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
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
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
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
    #Giveaway Dono Add
    @commands.command(aliases=['da'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def heist_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) (user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['hdr'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def heist_dono_remove(self, ctx, member: discord.Member, amount: int):
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
    @commands.command(aliases=['hdrs'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def heist_dono_reset(self, ctx, member: discord.Member):
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
    EVENT DONATIONS
    '''
    #Giveaway Dono Add
    @commands.command(aliases=['eda'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def event_dono_add(self, ctx, member: discord.Member, amount: int):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) (user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was **{amount}**")

        dbase.commit()
        dbase.close()

    #Dono Remove
    @commands.command(aliases=['edr'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def event_dono_remove(self, ctx, member: discord.Member, amount: int):
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
    @commands.command(aliases=['edrs'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164, 810233857768554506) 
    async def event_dono_reset(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')

        amount = 0

        cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount = ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note reset for **{member}**\nThe amount was set to **{amount}**")

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Dono(client))