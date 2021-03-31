import discord
from discord.ext import commands

class Dono(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Dono Check
    @client.command(aliases=['d'])
    async def dono(self, ctx, member: discord.Member):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        cursor.execute(f"SELECT amount FROM dono_logs WHERE guild_id = '{ctx.guild.id}' AND user_id = '{member.id}'")
        result = cursor.fetchone()

        if member is None:
            if result is None:
                embed = discord.Embed(title='Donation Stats', description=f'{member}s donation stats', color=0x00ff00)
                embed.add_field(name='User:', value=f'{member.mention}({member.id})', inline=False)
                embed.add_field(name='Donations:', value=f'{result} donated in {ctx.guild.name}')
                await ctx.send(embed=embed)

                dbase.commit()
                dbase.close()

            else:
                embed = discord.Embed(title='Donation Stats', description=f'{member}s donation stats', color=0x00ff00)
                embed.add_field(name='User:', value=f'{member.mention}({member.id})', inline=False)
                embed.add_field(name='Donations:', value=f'{result} donated in {ctx.guild.name}')
                await ctx.send(embed=embed)

                dbase.commit()
                dbase.close()

        else: 
            embed = discord.Embed(title='Donation Stats', description=f'{member}s donation stats', color=0x00ff00)
            embed.add_field(name='User:', value=f'{member.mention}({member.id})', inline=False)
            embed.add_field(name='Donations:', value=f'{result} donated in {ctx.guild.name}')
            await ctx.send(embed=embed)

            dbase.commit()
            dbase.close()

    #Dono Add
    @commands.command(aliases=['da'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164) 
    async def dono_add(self, ctx, member: discord.Member, amount):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note added for **{member}**\nThe amount added was {amount}")

        dbase.commit()
        dbase.close()

    @commands.command(aliases=['dr'])
    @commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164) 
    async def dono_remove(self, ctx, member: discord.Member, amount):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        guild = int(ctx.guild.id)
        user = int(f'{member.id}')
        amount = int(f'{amount}')

        cursor.execute("INSERT INTO dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount - ?;", [guild, user, amount, amount])

        await ctx.send(f"Donation note removed for **{member}**\nThe amount removed was {amount}")

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Dono(client))