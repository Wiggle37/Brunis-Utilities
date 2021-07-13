import discord
from discord.ext import commands
import asyncio
import sys
from datetime import datetime
import time

class Utility(commands.Cog, name='utility', description='Some commands that will be helpful when needed'):

    def __init__(self, bot):
        self.bot = bot

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
    async def ping(self, ctx: commands.Context):
        start = time.perf_counter()
        message = await ctx.send("🏓 Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000

        await message.edit(content = f"🏓 Pong! Current latency: `{duration:.2f} ms`")

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

    #Bot Info
    @commands.command()
    async def botinfo(self, ctx):
        msg = f'''
        ```asciidoc\n
=== {self.bot.user} Info ===

• Latency             :: {int(self.bot.latency * 1000)}ms
• Discord Version     :: {discord.__version__}
• Python Version Info :: {sys.version}
```
        '''

        await ctx.send(msg)

    #Bug
    @commands.command()
    async def bug(self, ctx, *, bug):
        wiggle = self.bot.get_user(824010269071507536)
        embed = discord.Embed(title='Bug Report', description=f'**Reporter:** {ctx.author}({ctx.author.id})\n\n{bug}', color=discord.Color.red())
        embed.timestamp = datetime.utcnow()
        await wiggle.send(embed=embed)
        await ctx.send('Bug sent!')
    
    #Suggest
    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        embed = discord.Embed(title=f'Suggestion From {ctx.author}', description=f'**Suggestion:**\n{suggestion}')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'User id: {ctx.author.id}')
        msg = await self.bot.get_channel(827293945003376650).send(embed=embed)
        await msg.add_reaction('✔')
        await msg.add_reaction('✖')
        await ctx.send('Suggestion sent in <#827293945003376650>')

def setup(bot):
    bot.add_cog(Utility(bot))