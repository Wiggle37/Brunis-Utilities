import discord
from discord import message
from discord.ext import commands
import sqlite3
import asyncio

class Sticky(commands.Cog, name='stickys'):

    def __init__(self, client):
        self.client = client

    #Sticky
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
            await self.client.get_channel(result[0]).send(embed=embed)

            messages = await message.channel.history(limit=5).flatten()
            await messages[2].delete()


        dbase.close()

    @commands.command(name='add_sticky', description='Add a stickied message to a channel')
    @commands.has_any_role(785202756641619999, 788738305365114880, 784492058756251669, 788738308879941633) # Bruni, Co-Owner, Admin, Bot Dev
    async def add_sticky(self, ctx):
        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel

        dbase = sqlite3.connect('stickys.db')
        cursor = dbase.cursor()

        try:
            await ctx.send('What do you want the name of this sticky to be so you can delete it or edit it in the future')
            name = await self.client.wait_for("message", check=check, timeout=30)
            cursor.execute(f"SELECT stickyname FROM stickys WHERE stickyname == ?", [name.content.lower()])
            result = cursor.fetchone()
            if result != None:
                return await ctx.send('This sticky is already a thing please try another name')

        except TimeoutError:
            return await ctx.send("You did't respond in time")

        try:
            await ctx.send('What channel do you want this to be in? **use the id not the channel mention**')
            channel = await self.client.wait_for("message", check=check, timeout=30)
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
            message = await self.client.wait_for("message", check=check, timeout=60)

        except TimeoutError:
            return await ctx.send("You didn't send the message in time")

        cursor.execute("INSERT INTO stickys (stickyname, channel_id, message) VALUES (?, ?, ?);", [name.content.lower(), channel.content, message.content.lower()])

        embed = discord.Embed(title='Sticky Added With The Following Details', description=f'Name: {name.content.lower()}\nChannel: {int(channel.content)}\n\nMessage: {message.content.lower()}')
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Sticky(client))