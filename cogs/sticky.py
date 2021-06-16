from os import name
import discord
from discord import message
from discord.ext import commands
import sqlite3
import asyncio

class Sticky(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Sticky
    @commands.Cog.listener()
    async def on_message(self, message):
        return

    @commands.command()
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

        cursor.execute(f"INSERT INTO stickys (channel_id, stickyname, message) VALUES (?, ?, ?)", [channel.content, name.content.lower(), message.content.lower()])

        embed = discord.Embed(title='Sticky Added With The Following Details', description=f'Name: {name}\nChannel: {channel}\n\nMessage: {message}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Sticky(client))