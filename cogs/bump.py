import discord
from discord.ext import commands
import re

import sqlite3

class BumpTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    
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

    @commands.Cog.listener()
    async def on_message(self, message):
        dbase = sqlite3.connect('bump.db')
        cursor = dbase.cursor()

        bump = 1
        user = message.author.id

        if not self.valid_message(message):
            return
        
        embed_desc = message.embeds[0].description
        success = self.check_success(embed_desc)
        if success == None:
            return
        user_id = self.get_user_id(embed_desc)

        if success:
            cursor.execute("INSERT INTO bumps (user_id, bump) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET bump = bump + ?;", [user_id, bump, bump])
            cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user_id, bump, bump])

        else:
            cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user_id, bump, bump])

        dbase.commit()
        dbase.close()

    #Check Bumps
    @commands.command()
    async def bumps(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('bump.db')
        cursor = dbase.cursor()

        if member is None:
            user = ctx.author.id
            bump = 0
            cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user, bump, bump])
            cursor.execute("INSERT INTO bumps (user_id, bump) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET bump = bump + ?;", [user, bump, bump])

            cursor.execute(f"SELECT bump FROM bumps WHERE user_id = '{ctx.author.id}'")
            successful = cursor.fetchone()
            successful = int(successful[0])

            cursor.execute(f"SELECT allbumps FROM bumps WHERE user_id = '{ctx.author.id}'")
            total = cursor.fetchone()
            total = int(total[0])

            embed = discord.Embed(title=f'Bumps for **{ctx.author}**', description='The server bump tracker', color=0x00ff00)
            embed.add_field(name='Successful Bumps:', value=f'`{successful}`')
            embed.add_field(name='Total Bumps:', value=f'`{total}`')
            await ctx.send(embed=embed)

        else:
            user = member.id
            bump = 0
            cursor.execute("INSERT INTO bumps (user_id, allbumps) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET allbumps = allbumps + ?;", [user, bump, bump])
            cursor.execute("INSERT INTO bumps (user_id, bump) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET bump = bump + ?;", [user, bump, bump])
            
            cursor.execute(f"SELECT bump FROM bumps WHERE user_id = '{member.id}'")
            successful = cursor.fetchone()
            successful = int(successful[0])

            cursor.execute(f"SELECT allbumps FROM bumps WHERE user_id = '{member.id}'")
            total = cursor.fetchone()
            total = int(total[0])

            embed = discord.Embed(title=f'Bumps for **{member}**', description='The server bump tracker', color=0x00ff00)
            embed.add_field(name='Successful Bumps:', value=f'`{successful}`')
            embed.add_field(name='Total Bumps:', value=f'`{total}`')
            await ctx.send(embed=embed)
        
        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(BumpTracker(client))