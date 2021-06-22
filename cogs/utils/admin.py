import discord
from discord.ext import commands
import sqlite3

class Admin(commands.Cog, name='Admin', description='Commands only admins can use'):

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

    @commands.command(name='add_auto_response', description='Add an auto response', aliases=['ara'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def ara(self, ctx, trigger, *, response):
        dbsae = sqlite3.connect('autoresponse.db')
        cursor = dbsae.cursor()

        cursor.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            cursor.execute(f"INSERT INTO text (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
            cursor.execute(f"UPDATE reactions SET response = ? WHERE trigger == '{trigger}'", [response])

            await ctx.send(f'A new Trigger has been added with the following information:\nTrigger: {trigger}\nResponse: {response}')

        else:
            await ctx.send('This trigger already exists')

        dbsae.commit()
        dbsae.close()

    @commands.command(name='remove_auto_response', description='Remove an auto response', aliases=['arr'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def arr(self, ctx, trigger):
        dbase = sqlite3.connect('autoresponse.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            await ctx.send("This trigger doesn't exist what are you doing?")

        elif exist[0] == trigger:
            cursor.execute(f"DELETE FROM text WHERE trigger == '{trigger}'")

            await ctx.send('Trigger Deleted')

        else:
            await ctx.send('That is not a trigger currently added')

        dbase.commit()
        dbase.close()

    #Emoji Add Auto Response
    @commands.command(name='add_auto_reaction', description='Add an emoji reaction', aliases=['aea'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def aea(self, ctx, trigger, emoji):
        dbase = sqlite3.connect('autoresponse.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT trigger FROM emoji WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            cursor.execute(f"INSERT INTO emoji (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
            cursor.execute(f"UPDATE emoji SET emoji = ? WHERE trigger == '{trigger}'", [emoji])

            await ctx.send('Emoji response added!')

        elif exist != None:
            return await ctx.send('This trigger already exists!')

        dbase.commit()
        dbase.close()

    @commands.command(name='remove_auto_reaction', description='Remove an emoji reaction', aliases=['aer'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def aer(self, ctx, trigger):
        dbase = sqlite3.connect('autoresponse.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT trigger FROM emoji WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            await ctx.send("This trigger doesn't exist what are you doing?")

        elif exist[0] == trigger:
            cursor.execute(f"DELETE FROM emoji WHERE trigger == '{trigger}'")

            await ctx.send('Trigger Deleted')

        else:
            await ctx.send('That is not a trigger currently added')

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Admin(client))