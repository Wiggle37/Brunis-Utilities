import discord
from discord.ext import commands

import aiosqlite
import sqlite3

from config import *
from buttons import *

class configuration(commands.Cog, name='Configuration'):
    def __init__(self, bot):
        self.bot = bot

    # Add Auto Reponse
    @commands.command(name='add_auto_response', description='Add an auto response', aliases=['ara'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def ara(self, ctx, trigger, *, response):
        view = ChosePremium()
        async with aiosqlite.connect('autoresponse.db') as dbase:
            cursor = await dbase.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
            exist = await cursor.fetchone()
            if exist is None:
                await dbase.execute(f"INSERT INTO text (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
                await dbase.execute(f"UPDATE text SET response = ? WHERE trigger == '{trigger}'", [response])
                await dbase.commit()

                await ctx.send(f'A new Trigger has been added with the following information:\nTrigger: {trigger}\nResponse: {response}', view=view)
                await view.wait()
                if view.value is None:
                    return await ctx.send('Timed out, this trigger will be useable by everyone in the server')
                
                elif view.value:
                    await dbase.execute(f"UPDATE text SET premium = ? WHERE trigger = '{trigger}'", [True])
                    await dbase.commit()
                    return await ctx.send('Ok, this trigger will only be usable by premium members')
                
                elif not view.value:
                    return await ctx.send('Ok, this trigger will be useable by all members of the server')

            elif exist is not None:
                await ctx.send('This trigger already exists')

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
        view = ChosePremium()
        async with aiosqlite.connect('autoresponse.db') as dbase:
            cursor = await dbase.execute(f"SELECT trigger FROM emoji WHERE trigger == ?", [trigger])
            exist = await cursor.fetchone()
            if exist is None:
                await dbase.execute(f"INSERT INTO emoji (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
                await dbase.execute(f"UPDATE emoji SET emoji = ? WHERE trigger = '{trigger}'", [emoji])
                await dbase.commit()

                await ctx.send('Emoji response added!', view=view)

                await view.wait()
                if view.value is None:
                    return await ctx.send('Response timed out, this trigger will be useable by all users')

                elif view.value:
                    dbase.execute(f"UPDATE emoji SET premium = ? WHERE trigger = '{trigger}'", [True])
                    await dbase.commit()
                    return await ctx.send('Ok, this trigger will only be useable by premium users')

                elif not view.value:
                    return await ctx.send('This trigger will be useable by all members of the server')

            elif exist is not None:
                return await ctx.send('This trigger already exists!')


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
            CONFIG["settings"]["heists"]["heistmode"] = mode
            with open('config.json', 'w') as file:
                json.dump(CONFIG, file, indent=4)
                f.close()
            await ctx.send(f'Heistmode set to `{mode}`')

def setup(bot):
    bot.add_cog(configuration(bot))