import discord
from discord.ext import commands
import json

from config import *

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    '''
    Auto Reponses
    '''
    # Add Auto Reponse
    @commands.command(name='add_auto_response', description='Add an auto response', aliases=['ara'])
    @commands.has_any_role(784492058756251669, 788738308879941633, 784528018939969577)
    async def ara(self, ctx, trigger, *, response):
        dbsae = sqlite3.connect('autoresponse.db')
        cursor = dbsae.cursor()

        cursor.execute(f"SELECT trigger FROM text WHERE trigger == ?", [trigger])
        exist = cursor.fetchone()
        if exist is None:
            cursor.execute(f"INSERT INTO text (trigger) VALUES (?) ON CONFLICT(trigger) DO UPDATE SET trigger = ?", [trigger, trigger])
            cursor.execute(f"UPDATE text SET response = ? WHERE trigger == '{trigger}'", [response])

            await ctx.send(f'A new Trigger has been added with the following information:\nTrigger: {trigger}\nResponse: {response}')

        else:
            await ctx.send('This trigger already exists')

        dbsae.commit()
        dbsae.close()

    # Remove Auto Response
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

    # Emoji Add Auto Response
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

    # Emoji Remove Response
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
            CONFIG["heistmode"] = mode
            with open('config.json', 'w') as file:
                json.dump(CONFIG, file, indent=4)
                f.close()
            await ctx.send(f'Heistmode set to `{mode}`')

def setup(bot):
    bot.add_cog(Settings(bot))