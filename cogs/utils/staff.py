import discord
from discord.ext import commands
from typing import Union

import aiosqlite
import sqlite3

from config import *
from buttons import *

class Staff(commands.Cog, name = "Staff", description = "Commands only staff can use"):
    def __init__(self, bot):
        self.bot = bot

    # Dump Role
    @commands.has_guild_permissions(manage_guild=True)
    @commands.command(name='dump', description='Shows all the members with a specified role')
    async def dump(self, ctx, role: discord.Role):
        msg = ''
        for member in role.members:
            msg += f'{member}({member.id})\n'

        msg_split = [msg[i:i+1900] for i in range(0, len(msg), 1900)]
        for info in msg_split:
            await ctx.send(f"```{info}```")

    # Role
    @commands.group(name='role', description='Add or remove a role from someone', invoke_without_command=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, *, role: discord.Role):
        if member.top_role < role:
            return await ctx.send("You're not higher in the role hierachy than the role you're trying to add")
        
        if role not in member.roles:
            await member.add_roles(role, reason=f'Moderator: {ctx.author}({ctx.author.id})')
            return await ctx.send(f'`{role.name}` added to **{member}**')

        elif role in member.roles:
            await member.remove_roles(role, reason=f'Moderator: {ctx.author}({ctx.author.id})')
            return await ctx.send(f'`{role.name}` removed from **{member}**')

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

        # add one since the user sent a message to invoke the command
        await ctx.channel.purge(limit = amount + 1)

        purge_embed = discord.Embed(title = "Purged Messages", description = f"{amount} message(s) purged", color = 0x00ff00)
        await ctx.send(embed = purge_embed, delete_after = 5)

    # Lock
    @commands.command(name = "lock", description = "Locks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def lock(self, ctx, channel: discord.TextChannel = None):
        unlocked_channel = channel or ctx.channel
        await unlocked_channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send("Channel locked")

    # Unlock
    @commands.command(name = "unlock", description = "Unlocks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        locked_channel = channel or ctx.channel
        await locked_channel.set_permissions(ctx.guild.default_role, send_messages = None)
        await ctx.send("Channel unlocked")

    # Ban
    @commands.command(name='ban', description='Ban someone from the current server')
    @commands.has_any_role(784527745539375164, 784492058756251669)
    async def ban(self, ctx, member: Union[discord.Member, discord.User], *, reason: str = None):
        # we typehint to a member/user since we can ban people out of the guild
        if ctx.author == member:
            return await ctx.send("You can't ban yourself")
        
        if not isinstance(member, discord.User) and ctx.author.top_role < member.top_role:
            return await ctx.send("You're lower than that person on the role hierachy")
        
        reason = f'Banned by: {ctx.author}({ctx.author.id})\nReason: {reason}'
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f'**{member}** was banned')
        except discord.Forbidden:
            return await ctx.send('I am not high enough in the role hierarchy to ban this user')

    # Kick
    @commands.command(name='kick', description='Kick someone from the server')
    @commands.has_any_role(784527745539375164, 784492058756251669)
    async def kick(self, ctx, member: discord.Member):
        if ctx.author == member:
            return await ctx.send("You can't kick yourself")
        
        if ctx.author.top_role < member.top_role:
            return await ctx.send("You're lower than that person on the role hierachy")
        
        try:
            await member.kick(reason=f'Moderator: {ctx.author}({ctx.author.id})')
            await ctx.send(f'**{member}** was kicked')
        except discord.Forbidden:
            return await ctx.send('I am not high enough in the role hierarchy to kick this user')

def setup(bot):
    bot.add_cog(Staff(bot))
