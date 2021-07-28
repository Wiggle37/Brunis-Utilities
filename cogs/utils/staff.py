from os import error
import discord
from discord.ext import commands

import aiosqlite
import sqlite3

from config import *
from buttons import *

class Staff(commands.Cog, name = "Staff", description = "Commands only staff can use"):
    def __init__(self, bot):
        self.bot = bot

    # Add Overides
    @commands.command(name='addoveride', aliases=['ao'])
    @commands.is_owner()
    async def addoveride(self, ctx):
        num = 0
        num_ = 0
        errors = ''
        msg = await ctx.send('Attempting to add overides to all channels')
        for channel in ctx.guild.text_channels:
            try:
                await msg.edit(content=f'Channels Updated: {num}\nFailed Channel Updates: {num_}')
                await channel.set_permissions(ctx.me, read_messages=True, send_messages=True, embed_links=True, add_reactions=True, external_emojis=True, manage_permissions=True)
                
                num += 1

            except:
                num_ += 1
                errors += f'Error Updating: {channel.name}\n'

        tb_split = [errors[i:i+1990] for i in range(0, len(errors), 1990)]
        # sends each one
        for info in tb_split:
            await ctx.send(f"```{info}\n```")
        await ctx.send(f'{num} channels updated')

    # Dump Role
    @commands.command(name='dump', description='Shows all the members with a specified role')
    @commands.is_owner()
    async def dump(self, ctx, role: discord.Role):
        msg = ''
        for member in role.members:
            msg += f'{member.name}({member.id})\n'

        msg_split = [msg[i:i+1900] for i in range(0, len(msg), 1900)]
        # sends each one
        for info in msg_split:
            await ctx.send(f"```py\n{info}```")

    # Add Roles
    @commands.command(name = "addrole", description = "Adds role(s) to a member", aliases = ["ar"])
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"Role added to **{member}**")

    # Remove Roles
    @commands.command(name = "removerole", description = "Removes role(s) from a member", aliases = ["rr"])
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"Role removed from **{member}**")

    # Purge
    @commands.command(name = "purge", description = "Delete a certain amount of messages given")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def purge(self, ctx, amount: int = 1):
        if amount > 500:
            return await ctx.send(f"Purge less than 500 messages please")

        await ctx.message.delete()
        await ctx.channel.purge(limit = amount)

        purge_embed = discord.Embed(title = "Purged Messages", description = f"{amount} message(s) purged", color = 0x00ff00)
        await ctx.send(embed = purge_embed, delete_after = 1)

    # Lock
    @commands.command(name = "Lock", description = "Locks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send("Channel locked")

    # Unlock
    @commands.command(name = "unlock", description = "Unlocks the current channel for @\u200beveryone")
    @commands.has_any_role(784492058756251669, 784527745539375164) # Admin, Mod
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

    '''
    Stickys
    '''
    # Sticky
    @commands.Cog.listener()
    async def on_message(self, message):
        dbase = sqlite3.connect('stickys.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT channel_id FROM stickys WHERE channel_id == '{message.channel.id}'")
        result = cursor.fetchone()
        if result != None and not message.author.bot:
            cursor.execute(f"SELECT message FROM stickys WHERE channel_id == '{message.channel.id}'")
            msg = cursor.fetchone()

            embed = discord.Embed(title='Stickied Message', description=f'{msg[0]}', color=0x00ff00)
            await self.bot.get_channel(result[0]).send(embed=embed)

            messages = await message.channel.history(limit=5).flatten()
            await messages[2].delete()


        dbase.close()

    # Add Sticky
    @commands.command(name='add_sticky', description='Add a stickied message to a channel')
    @commands.has_any_role(785202756641619999, 788738305365114880, 784492058756251669, 788738308879941633) # Bruni, Co-Owner, Admin, Bot Dev
    async def add_sticky(self, ctx):
        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        dbase = sqlite3.connect('stickys.db')
        cursor = dbase.cursor()

        try:
            await ctx.send('What do you want the name of this sticky to be so you can delete it or edit it in the future')
            name = await self.bot.wait_for("message", check=check, timeout=30)
            cursor.execute(f"SELECT stickyname FROM stickys WHERE stickyname == ?", [name.content.lower()])
            result = cursor.fetchone()
            if result != None:
                return await ctx.send('This sticky is already a thing please try another name')

        except TimeoutError:
            return await ctx.send("You did't respond in time")

        try:
            await ctx.send('What channel do you want this to be in? **use the id not the channel mention**')
            channel = await self.bot.wait_for("message", check=check, timeout=30)
            if not channel.content.isdigit():
                return await ctx.send("That isnt't a valid number")
            
            else:
                channelCheck = discord.utils.find(lambda chan: chan.id == int(channel.content), ctx.guild.text_channels)
                if channelCheck is None:
                    return await ctx.reply("That channel doesn't exist")

        except TimeoutError:
            return await ctx.send("You didn't respond in time")

        try:
            await ctx.send('What do you want the message to be?')
            message = await self.bot.wait_for("message", check=check, timeout=60)

        except TimeoutError:
            return await ctx.send("You didn't send the message in time")

        cursor.execute("INSERT INTO stickys (stickyname, channel_id, message) VALUES (?, ?, ?);", [name.content.lower(), channel.content, message.content.lower()])

        embed = discord.Embed(title='Sticky Added With The Following Details', description=f'Name: {name.content.lower()}\nChannel: {int(channel.content)}\n\nMessage: {message.content.lower()}')
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

def setup(bot):
    bot.add_cog(Staff(bot))
