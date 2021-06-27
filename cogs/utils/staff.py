import discord
from discord.ext import commands
import sqlite3

class Admin(commands.Cog, name='admin', description='Commands only admins can use'):

    def __init__(self, client):
        self.client = client

    #Add Role
    @commands.command(name='addrole', description='Adds a role to a member', aliases=['ar'])
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633, 840738395001323563) #Admin, Mod, Bruni, Bot Dev
    async def addrole(self, ctx, member: discord.Member, *, role:discord.Role):
        await member.add_roles(role)
        await ctx.send(f'Role added to **{member}**')

    #Remove Role
    @commands.command(name='removerole', description='Removes a role from a member', aliases=['rr'])
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633, 840738395001323563) #Admin, Mod, Bruni, Bot Dev
    async def removerole(self, ctx, member: discord.Member, *, role:discord.Role):
        await member.remove_roles(role)
        await ctx.send(f'Role removed from **{member}**')

    #Purge
    @commands.command(name='purge', description='Delete a certain amount of messages given')
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633, 840738395001323563) #Admin, Mod, Bruni, Bot Dev
    async def purge(self, ctx, amount=1):
        if amount > 1000:
            await ctx.send(f'Please choose a number under 1000 to purge.\nYour number was: {amount}')

        else:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)

            purge_embed = discord.Embed(title='Purged Messages', description=f'{amount} message(s) purged', color=0x00ff00)
            await ctx.send(embed=purge_embed, delete_after=1)

    #Lock
    @commands.command(name='lock', description='Locks the current channel to everyone')
    @commands.has_any_role(791516118120267806)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send('Channel locked')

    #Unlock
    @commands.command(name='unlock', description='Unlocks the current channel to everyone')
    @commands.has_any_role(791516118120267806)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send('Channel unlocked')

def setup(client):
    client.add_cog(Admin(client))