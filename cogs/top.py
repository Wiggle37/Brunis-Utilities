import discord
from discord import embeds
from discord.ext import commands
import sqlite3
from discord.ext.commands.core import before_invoke

class Top(commands.Cog):

    def __init__(self, client):
        self.client = client

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
    client.add_cog(Top(client))
