import discord
from discord.ext import commands
import aiosqlite

from config import *

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


        '''
    Auto Reponses
    '''
    # Add Auto Reponse
    @commands.command(name='add_auto_response', description='Add an auto response', aliases=['ara'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def ara(self, ctx, trigger, *, response):
        dbsae = await aiosqlite.connect('autoresponse.db')
        cursor = await dbsae.cursor()

        await cursor.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            await cursor.execute(f"INSERT INTO text (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
            await cursor.execute(f"UPDATE text SET response = ? WHERE trigger == '{trigger}'", [response])

            await ctx.send(f'A new Trigger has been added with the following information:\nTrigger: {trigger}\nResponse: {response}')

        else:
            await ctx.send('This trigger already exists')

        await dbsae.commit()
        await dbsae.close()

    # Remove Auto Response
    @commands.command(name='remove_auto_response', description='Remove an auto response', aliases=['arr'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def arr(self, ctx, trigger):
        dbase = await aiosqlite.connect('autoresponse.db')
        cursor = await dbase.cursor()

        await cursor.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
        exist = await cursor.fetchone()
        if exist is None:
            await ctx.send("This trigger doesn't exist what are you doing?")

        elif exist[0] == trigger:
            await cursor.execute(f"DELETE FROM text WHERE trigger == '{trigger}'")

            await ctx.send('Trigger Deleted')

        else:
            await ctx.send('That is not a trigger currently added')

        await dbase.commit()
        await dbase.close()

    # Emoji Add Auto Response
    @commands.command(name='add_auto_reaction', description='Add an emoji reaction', aliases=['aea'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def aea(self, ctx, trigger, emoji):
        dbase = await aiosqlite.connect('autoresponse.db')
        cursor = await dbase.cursor()

        await cursor.execute(f"SELECT trigger FROM emoji WHERE trigger == ?", [trigger])
        exist = await cursor.fetchone()
        if exist is None:
            await cursor.execute(f"INSERT INTO emoji (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
            await cursor.execute(f"UPDATE emoji SET emoji = ? WHERE trigger == '{trigger}'", [emoji])

            await ctx.send('Emoji response added!')

        elif exist != None:
            return await ctx.send('This trigger already exists!')

        await dbase.commit()
        await dbase.close()

    # Emoji Remove Response
    @commands.command(name='remove_auto_reaction', description='Remove an emoji reaction', aliases=['aer'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def aer(self, ctx, trigger):
        dbase = await aiosqlite.connect('autoresponse.db')
        cursor = await dbase.cursor()

        await cursor.execute(f"SELECT trigger FROM emoji WHERE trigger == ?", [trigger])
        exist = await cursor.fetchone()
        if exist is None:
            await ctx.send("This trigger doesn't exist what are you doing?")

        elif exist[0] == trigger:
            await cursor.execute(f"DELETE FROM emoji WHERE trigger == '{trigger}'")

            await ctx.send('Trigger Deleted')

        else:
            await ctx.send('That is not a trigger currently added')

        await dbase.commit()
        await dbase.close()

    '''
    Heist Settings
    '''
    # Heist Mode
    @commands.command()
    @commands.has_any_role(784527745539375164, 784492058756251669, 788738305365114880, 788738308879941633) # Mod, Admin, Co-Owner, Bot dev
    async def heistmode(self, ctx, mode=True):
        types = [True, False]
        if mode not in types:
            return await ctx.send('That is not a valid option plese user either: `True` or `False`')

        elif mode or not mode:
            CONFIG["config"]["settings"]["heistmode"] = mode
            with open('config.json', 'w') as file:
                json.dump(CONFIG, file, indent=4)
                f.close()
            await ctx.send(f'Heistmode set to `{mode}`')

def setup(bot):
    bot.add_cog(Staff(bot))
