import discord
from discord.ext import commands
import asyncio

class Utility(commands.Cog, name='utility', description='Some commands that will be helpful when needed'):

    def __init__(self, client):
        self.client = client

    #Timer
    @commands.command(name='timer', description='Set a timer for up to 1000')
    async def count(self, ctx, number: int):
        try:
            if number < 0:
                await ctx.send('Must be a positve number')
            elif number > 1000:
                await ctx.send('Number must be under 1000')
            else:
                message = await ctx.send(number)
                while number != 0:
                    number -= 1
                    await message.edit(content=number)
                    await asyncio.sleep(1)
                await message.edit(content='Ended!')

        except ValueError:
            await ctx.send('Please provide a valid number')

    #Ping
    @commands.command(name='ping', description='Shows the bots current ping', aliases=['ms'])
    async def ping(self, ctx):
        await ctx.send(f'🏓 Current latency: `{int(self.client.latency * 1000)} ms`')

    #Server Info
    @commands.command(name='serverinfo', description='Shows the servers info', aliases=['si', 'server'])
    async def serverinfo(self, ctx):
        members = 0
        for member in ctx.guild.members:
            if not member.bot:
                members += 1
            else:
                pass

        total = (ctx.guild.member_count)

        info_embed = discord.Embed(title='Server Info/Stats', description='Here is the list of stats for the server', color=discord.Color.green())
        info_embed.set_thumbnail(url=ctx.guild.icon_url)
        info_embed.add_field(name='Server Name', value=ctx.guild.name)
        info_embed.add_field(name='Server Owner:', value=ctx.guild.owner)
        info_embed.add_field(name='Server ID', value=ctx.guild.id)
        info_embed.add_field(name='Server Human Count', value=members)
        info_embed.add_field(name='Total Member Count', value=total)
        await ctx.send(embed=info_embed)

def setup(client):
    client.add_cog(Utility(client))