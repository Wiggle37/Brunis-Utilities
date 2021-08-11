import discord
from discord.ext import commands

import aiosqlite
import sqlite3

from config import *
from buttons import *

class Staff(commands.Cog, name = "Staff", description = "Commands only staff can use"):
    def __init__(self, bot):
        self.bot = bot

    # Dump Role
    @commands.command(name='dump', description='Shows all the members with a specified role')
    async def dump(self, ctx, role: discord.Role):
        msg = ''
        for member in role.members:
            msg += f'{member.name}({member.id})\n'

        msg_split = [msg[i:i+1900] for i in range(0, len(msg), 1900)]
        for info in msg_split:
            await ctx.send(f"```py\n{info}```")

    # Role
    @commands.group(name='role', description='Add or remove a role from someone', invoke_without_command=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):
        if role not in member.roles:
            await member.add_roles(role)
            return await ctx.send(f'`{role.name}` added to **{member.name}**')

        elif role in member.roles:
            await member.remove_roles(role)
            return await ctx.send(f'`{role.name}` removed from **{member.name}**')

    @role.command(name='info', description='Get info on a role')
    async def info(self, ctx, *, role: discord.Role):
        embed = discord.Embed(title=f'{role.name} info', color=role.color)
        embed.add_field(name='Members', value=len(role.members))
        embed.add_field(name='Color', value=role.color)
        embed.add_field(name='Created', value=f'<t:{int(role.created_at.timestamp())}>')
        embed.add_field(name='Permissions', value=f'[{role.permissions.value}](https://discordapi.com/permissions.html#{role.permissions.value})')
        embed.add_field(name='Position', value=role.position)
        embed.add_field(name='ID and Mention', value=f'{role.id}\n`{role.mention}`')

        embed.add_field(name='Managed By Bot', value=role.is_bot_managed())
        embed.add_field(name='Managed By Boosts', value=role.is_premium_subscriber())
        embed.add_field(name='Is Assignable', value=role.is_assignable())
        await ctx.send(embed=embed)

    # Purge
    @commands.command(name = "purge", description = "Delete a certain amount of messages given")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def purge(self, ctx, amount: int = 1):
        if amount > 500:
            return await ctx.send(f"Purge less than 500 messages please")

        await ctx.channel.purge(limit = amount)

        purge_embed = discord.Embed(title = "Purged Messages", description = f"{amount} message(s) purged", color = 0x00ff00)
        await ctx.send(embed = purge_embed, delete_after = 5)

    # Lock
    @commands.command(name = "lock", description = "Locks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def lock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        elif channel is not None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send("Channel locked")

    # Unlock
    @commands.command(name = "unlock", description = "Unlocks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def unlock(self, ctx, channel: discord.TextChannel):
        if channel is None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = None)
        elif channel is not None:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = None)
        await ctx.send("Channel unlocked")
   

def setup(bot):
    bot.add_cog(Staff(bot))
