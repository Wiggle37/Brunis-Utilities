import discord
from discord.ext import commands

import aiosqlite
import sqlite3
import asyncio

from config import *
from buttons import *

class Staff(commands.Cog, name = "Staff", description = "Commands only staff can use"):
    def __init__(self, bot):
        self.bot = bot
        self.ignored_channels = [
            784530970220953660, # Welcome
            792948346268286986, # Vote For Us
            822567848400388106, # Big Heist Channel
            787343840108478474, # Rules
            784547669619507201, # Self Roles
            787390795182506005, # FAQ
            854845899493474364, # Role Perks
            863437182131503134, # Grinder Perks
            827293945003376650, # BUtils Updates
            787737517901217893, # Apply For Staff
            800371218242601000, # Booster Shoutout
            787385929987522560, # Staff Intro
            818667976316289024, # Server Change Log
            868358619043889172, # Ban Appeal
            787761394664996865, # Support
            861928682825711616, # Trade Rules
            787760571972845568, # Scammer Alert
            787817916820357161, # Sale Item
            785338471639547918, # Bot News
            785159189022244894, # Bot Tips
            797304436175273994, # Prestige Here
            861939728324755456, # Fight Rules
            795122854613614614, # Donation Info
            796200850908774411, # Events Info
            784494364754706462, # Events
            850526312865988638, # Mafia
            861580122984546315, # Rumble
            789227950636793887, # Auction Court
            789227726355562547, # Auction Rule
        ]
        
        self.ignored_categories = [
            788160365711458314, # Private Property
            848216650306289704, # Giveaway Managing
            784498914073116692, # Staff
            826893902984118272, # Gambling
            788764981957099520, # Archived
            788010175402344448, # Fun
            854730780785115167, # Leveling
            848038640566403102, # Partnership
            784494228084228157, # Events
            796200447571787826, # Heists
            784535143250788352, # Giveaways
        ]

    # Lockdown
    @commands.command()
    @commands.is_owner()
    async def lockdown(self, ctx):
        merchants = self.bot.get_guild(784491141022220309)
        view = Confirm(ctx.author.id)
        success = 0
        failed = 0
        failed_channels = []

        async with ctx.typing():
            await ctx.send('Are you sure you want to lockdown the server for staffday?', view=view)
            await view.wait()
            if view.value is None:
                return await ctx.send('Timed out...')
            
            if view.value:
                msg = await ctx.send('Attempting to lock all channels...')
                await asyncio.sleep(2)
                for channel in merchants.text_channels:
                    try:
                        if not channel.category.id in self.ignored_categories and channel.id not in self.ignored_channels:
                            await channel.set_permissions(merchants.default_role, send_messages=False)
                            success += 1
                            await msg.edit(content=f'Success: {success}\nFailed: {failed}')
                        else:
                            continue
                    except Exception as error:
                        await ctx.send(error)
                        failed_channels.append(channel.name)
                        failed += 1
                        await msg.edit(content=f'Success: {success}\nFailed: {failed}')
                if len(failed_channels) > 0:
                    await ctx.send(f'Done locking channels, however there were a few channels that could not be updated due to a lack of permissions\nFailed Channels: {", ".join(failed_channels)}')
                elif len(failed_channels) == 0:
                    await ctx.send('Done updating all channels, there were no problems along the way!')

            if not view.value:
                return await ctx.send('Ok, cancelled')

    # Dump Role
    @commands.command(name='dump', description='Shows all the members with a specified role')
    async def dump(self, ctx, role: discord.Role):
        msg = ''
        for member in role.members:
            msg += f'{member.name}({member.id})\n'

        msg_split = [msg[i:i+1900] for i in range(0, len(msg), 1900)]
        # sends each one
        for info in msg_split:
            await ctx.send(f"```py\n{info}```")


    # Role
    @commands.group(name='role', description='Add or remove a role from someone', invoke_without_command=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        if role not in member.roles:
            await member.add_roles(role)
            return await ctx.send(f'`{role.name}` added to **{member.name}**')

        elif role in member.roles:
            await member.remove_roles(role)
            return await ctx.send(f'`{role.name}` removed from **{member.name}**')

    @role.command(name='info', description='Get info on a role')
    async def info(self, ctx, role: discord.Role):
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
