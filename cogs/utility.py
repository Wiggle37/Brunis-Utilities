import discord
from discord.ext import commands
import asyncio
import sqlite3

class Utility(commands.Cog, name='Utility', description='Some commands that will be helpful when needed'):

    def __init__(self, client):
        self.client = client

    #Timer
    @commands.command()
    async def count(self, ctx, number: int):
        client = self.client
        try:
            if number < 0:
                await ctx.send('Must be a positve number')
            elif number > 1000:
                await ctx.send('Number must be under 1000')
            else:
                message = await ctx.send(number)
                while number != 0:
                    number -= 1
                    await message.edit(content=number)
                    await asyncio.sleep(1)
                await message.edit(content='Ended!')

        except ValueError:
            await ctx.send('Please provide a valid number')

    #Giveaway announcement
    @commands.command()
    @commands.has_role(785198646731604008)
    async def gaw(self, ctx, sponser: discord.Member=None, *, msg='No message provided'):
        if sponser == None:
            await ctx.send('You have to provide a sponser', delete_after=3)

        else:
            await ctx.message.delete()
            embed = discord.Embed(title=f'Giveaway Donated By {sponser}!', description=f'Message: {msg}', color=0x00ff00)
            embed.add_field(name='More info:', value=f'- Make sure to thank {sponser.mention} in <#784491141022220312>\n- Go to <#785154861922254848> to donate for giveaways\n- Go to <#818269054103978004> to donate for heists')
            embed.set_thumbnail(url='https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/video/uh59Wh0/stacks-of-money-with-coins-cartoon-illustration-hand-drawn-animation-transparent-cartoon-illustration-hand-drawn-animation-transparent_s289_zlf_thumbnail-1080_07.png')
            await ctx.send('<@&785930653665067038>', embed=embed)

    @commands.command()
    async def tops(self, ctx, board='donor'):
        if board.lower() == 'donor' or board.lower() == 'dank' or board.lower() == 'donors' or board.lower() == 'total':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, total FROM donations ORDER BY total DESC")
            dank_donors = cursor.fetchmany(25)

            top_donors_embed = discord.Embed(title="Top Total donors!", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Dank Memer Donations Leader Board**__\n"
            dank_merchants = self.client.get_guild(784491141022220309)
            for rank, user in enumerate(dank_donors):
                member = dank_merchants.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'money' or board.lower() == 'moneys':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, money FROM donations ORDER BY money DESC")
            money_donors = cursor.fetchmany(5)

            top_donors_embed = discord.Embed(title="Top Money Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Real Money Donations Leader Board**__\n"
            for rank, user in enumerate(money_donors):
                member = ctx.guild.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `${'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'bumps' or board.lower() == 'bump':
            dbase = sqlite3.connect("bump.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, bump FROM bumps ORDER BY bump DESC")
            bumpers = cursor.fetchmany(10)

            top_bumpers_embed = discord.Embed(title="Top Bumpers", color=0x00ff00)
            bumper_info = ""

            bumper_info += "__**Server Bumps Leader board**__\n"
            dank_merchants = self.client.get_guild(784491141022220309)
            for rank, user in enumerate(bumpers):
                member = dank_merchants.get_member(int(user[0]))
                bumper_info += f"**{rank + 1}. {member}**: `{'{:,}'.format(user[1])}`\n"
            
            top_bumpers_embed.description=bumper_info
            dbase.close()
            
            return await ctx.send(embed=top_bumpers_embed)
        
        if board.lower() == 'special':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, special FROM donations ORDER BY special DESC")
            special_donors = cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Special Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Special Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = ctx.guild.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'heist':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, heist FROM donations ORDER BY heist DESC")
            special_donors = cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Heist Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Heist Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = ctx.guild.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'event':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, event FROM donations ORDER BY event DESC")
            special_donors = cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Event Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Event Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = ctx.guild.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

        if board.lower() == 'gaw' or board.lower() == 'givaway':
            dbase = sqlite3.connect("dono.db")
            cursor = dbase.cursor()

            cursor.execute("SELECT user_id, gaw FROM donations ORDER BY gaw DESC")
            special_donors = cursor.fetchmany(10)

            top_donors_embed = discord.Embed(title="Top Giveaway Donators", color=0x00ff00)
            donor_info = ""

            donor_info += "__**Giveaway Donations Leader Board**__\n"
            for rank, user in enumerate(special_donors):
                member = ctx.guild.get_member(int(user[0]))
                donor_info += f"**{rank + 1}. {member}**: `⏣{'{:,}'.format(user[1])}`\n"

            top_donors_embed.description=donor_info
            dbase.close()
            return await ctx.send(embed=top_donors_embed)

def setup(client):
    client.add_cog(Utility(client))