import discord
from discord.ext import commands
import time

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Add Role
    @commands.command(aliases=['ar'])
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633) #Admin, Mod, Bruni, Bot Dev
    async def addrole(self, ctx, member: discord.Member=None, *, role:discord.Role=None):
        client = self.client
        await member.add_roles(role)
        await ctx.send(f'Role added to **{member}**')

    #Remove Role
    @commands.command(aliases=['rr'])
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633) #Admin, Mod, Bruni, Bot Dev
    async def removerole(self, ctx, member: discord.Member=None, *, role:discord.Role=None):
        client = self.client
        await member.remove_roles(role)
        await ctx.send(f'Role removed from **{member}**')

    #Purge
    @commands.command()
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633) #Admin, Mod, Bruni, Bot Dev
    async def purge(self, ctx, amount=1):
        if amount > 1000:
            await ctx.send(f'Please choose a number under 1000 to purge.\nYour number was: {amount}')

        else:

            await ctx.message.delete()

            await ctx.channel.purge(limit=amount)

            purge_embed = discord.Embed(title='Purged Messages', description=f'{amount} message(s) purged', color=0x00ff00)
            await ctx.send(embed=purge_embed)

            time.sleep(2)

            await ctx.channel.purge(limit=1)

    #Lock
    @commands.command()
    @commands.has_any_role(794292540806791229)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send('Channel locked')

    @lock.error
    async def error(self, ctx, error):
        await ctx.send(f'There was an error\n{error}')

    #Unlock
    @commands.command()
    @commands.has_any_role(794292540806791229)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send('Channel unlocked')

    @unlock.error
    async def error(self, ctx, error):
        await ctx.send(f'There was an error\n{error}')

def setup(client):
    client.add_cog(Admin(client))