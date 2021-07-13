import discord
from discord.ext import commands
import traceback, sys

class Staff(commands.Cog, name = "Admin", description = "Commands only staff can use"):
    def __init__(self, bot):
        self.bot = bot

    # Add Roles
    @commands.command(name = "addrole", description = "Adds role(s) to a member", aliases = ["ar"])
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def addrole(self, ctx, member: discord.Member, roles: commands.Greedy[discord.Role]):
        await member.add_roles(roles)
        await ctx.send(f"Role added to **{member}**")

    # Remove Roles
    @commands.command(name = "removerole", description = "Removes role(s) from a member", aliases = ["rr"])
    @commands.has_any_role(784492058756251669, 784527745539375164) #Admin, Mod
    async def removerole(self, ctx, member: discord.Member, roles: commands.Greedy[discord.Role]):
        await member.remove_roles(roles)
        await ctx.send(f"Role removed from **{member}**")

    # Purge
    @commands.command(name = "purge", description = "Delete a certain amount of messages given")
    @commands.has_any_role(784492058756251669, 784527745539375164) #Admin, Mod
    async def purge(self, ctx, amount: int = 1):
        if amount > 500:
            return await ctx.send(f"Purge less than 500 messages please")

        await ctx.message.delete()
        await ctx.channel.purge(limit = amount)

        purge_embed = discord.Embed(title = "Purged Messages", description = f"{amount} message(s) purged", color = 0x00ff00)
        await ctx.send(embed = purge_embed, delete_after = 1)

    # Lock
    @commands.command(name = "Lock", description = "Locks the current channel for @\u200beveryone")
    @commands.has_any_role(791516118120267806) # staff
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send("Channel locked")

    # Unlock
    @commands.command(name = "unlock", description = "Unlocks the current channel for @\u200beveryone")
    @commands.has_any_role(791516118120267806) # staff
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send("Channel unlocked")

def setup(bot):
    bot.add_cog(Staff(bot))
