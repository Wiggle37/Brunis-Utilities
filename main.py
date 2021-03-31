###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import os
from dotenv import load_dotenv

import sqlite3

###Intents###
intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(
    shard_count=3,
    command_prefix='b!',
    intents=intents,
    case_insensitive=True,
    )
client.remove_command('help')

###On Ready###
@client.event
async def on_ready():
    print('Bot Online!')

roles = [
    'giveaways'
]

#Dono Check
@client.command(aliases=['d'])
async def dono(ctx, member: discord.Member):
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
@client.command(aliases=['da'])
@commands.has_any_role(785198646731604008, 785631914010214410, 784527745539375164) 
async def dono_add(ctx, member: discord.Member, amount):
    dbase = sqlite3.connect('dono.db')
    cursor = dbase.cursor()

    guild = int(ctx.guild.id)
    user = int(f'{member.id}')
    amount = int(f'{amount}')

    cursor.execute("INSERT INTO dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])


    await ctx.send(f"Donation note added for **{member}**\nThe amount added was {amount}")

    dbase.commit()
    dbase.close()

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('Discord_Bot_Token')
client.run(Bot_Token)