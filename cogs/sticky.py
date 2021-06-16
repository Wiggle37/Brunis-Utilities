import discord
from discord.ext import commands
import sqlite3

class Sticky(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Sticky
    @commands.Cog.listener()
    async def on_message(self, message):
        return

    @commands.command()
    async def add_sticky(self, ctx, channel: int, name, *, message):
        dbase = sqlite3.connect('stickys.db')
        cursor = dbase.cursor()

        channel = discord.utils.find(ctx.guild.text_channels, id=channel)
        if channel is None:
            return await ctx.reply("That channel doesn't exist")

        cursor.execute(f"SELECT name FROM stickys WHERE name == '{name}'")
        exist = cursor.fetchone()
        if exist is None:
            cursor.execute(f"INSERT INTO stickys (channel_id, stickyname, message) VALUES (?, ?, ?)", [channel, name, message])

        else:
            return await ctx.send('This sticky already exists try naming it something else')

def setup(client):
    client.add_cog(Sticky(client))