import discord
from discord.ext import commands

import re
import aiosqlite

from config import *

class BumpTracker(commands.Cog, name='bumps', description='Tracks how much the server gets bumped'):
    def __init__(self, bot):
        self.bot = bot

    # Check Bumps
    @commands.command(name='bumps', description='Check the amount of successful and unsuccessful bumps you have in the server', aliases=['b', 'bump'])
    async def bumps(self, ctx, member: discord.Member=None):
        dbase = await aiosqlite.connect('bump.db')
        cursor = await dbase.cursor()
        user = (member or ctx.author).id
        await cursor.execute(f"INSERT INTO bumps (user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET user_id = ?;", [user, user])
        await cursor.execute(f"SELECT bump FROM bumps WHERE user_id = '{user}'")
        bump = await cursor.fetchone()[0]
        await cursor.execute(f"SELECT allbumps FROM bumps WHERE user_id = '{user}'")
        total = await cursor.fetchone()[0]
        user = await ctx.guild.fetch_member(user)

        if bump == 0:
            embed = discord.Embed(title=f'Bumps for **{user}**', description='The server bump tracker', color=0x00ff00)
            embed.add_field(name='Successful Bumps:', value=f'`{int(bump)}`')
            embed.add_field(name='Total Bumps:', value=f'`{(total)}`')
            embed.set_footer(text='Big thanks to Firecracker for helping with the bump system')
            await ctx.send(embed=embed)

        else:
            percentage = int(round(bump / total, 2) * 100)

            embed = discord.Embed(title=f'Bumps for **{user}**', description='The server bump tracker', color=0x00ff00)
            embed.add_field(name='Successful Bumps:', value=f'`{int(bump)}`')
            embed.add_field(name='Total Bumps:', value=f'`{(total)}`')
            embed.add_field(name='Percentage:', value=f'`{int(percentage)}%`')
            embed.set_footer(text='Big thanks to Firecracker for helping with the bump system')
            await ctx.send(embed=embed)
        
        await dbase.close()

    def valid_message(self, message):
        return message.author.id == 302050872383242240 and message.channel.id == 784994978661138453 and message.embeds != [] 
    
    def check_success(self, desc):
        if "Bump done :thumbsup:" in desc:
            return True
        elif "Please wait another" in desc:
            return False
        return None    

    def get_user_id(self,desc):
        return int(re.search(re.compile(r"\d{17,19}"), desc)[0])

    # Bump Listener
    @commands.Cog.listener()
    async def on_message(self, message):
        dbase = await aiosqlite.connect('bump.db')
        cursor = await dbase.cursor()

        bump = 1

        if not self.valid_message(message):
            return
        
        embed_desc = message.embeds[0].description
        success = self.check_success(embed_desc)

        if success == None:
            return

        user_id = self.get_user_id(embed_desc)

        if success:
            await cursor.execute("INSERT INTO bumps (user_id, bump) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET bump = bump + ?;", [user_id, bump, bump])
            await cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user_id, bump, bump])

            await cursor.execute(f"SELECT bump FROM bumps WHERE user_id = '{user_id}'")
            bump = await cursor.fetchone()

            await cursor.execute(f"SELECT allbumps FROM bumps WHERE user_id = '{user_id}'")
            total = await cursor.fetchone()

            precentage = int(round(bump[0] / total[0], 2) * 100)

            await cursor.execute(f"UPDATE bumps SET precentage = '{precentage}' WHERE user_id == {user_id}")

        else:
            await cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user_id, bump, bump])
            
            await cursor.execute(f"SELECT bump FROM bumps WHERE user_id = '{user_id}'")
            bump = await cursor.fetchone()

            await cursor.execute(f"SELECT allbumps FROM bumps WHERE user_id = '{user_id}'")
            total = await cursor.fetchone()

            precentage = int(round(bump[0] / total[0], 2) * 100)

            await cursor.execute(f"UPDATE bumps SET precentage = '{precentage}' WHERE user_id == {user_id}")

        cursor.execute("SELECT user_id, MAX(bump) FROM bumps;")
        top = cursor.fetchone()
        top = int(top[0])

        role = discord.utils.find(lambda r: r.id == 787868761620348929, message.guild.roles)

        user = await message.guild.fetch_member(top)
            
        if role in user.roles:
            await user.remove_roles(role)

        await user.add_roles(role)

        await dbase.commit()
        await dbase.close()

def setup(bot):
    bot.add_cog(BumpTracker(bot))