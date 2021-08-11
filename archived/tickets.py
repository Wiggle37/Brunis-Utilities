import discord
from discord.ext import commands

from config import *
from buttons import *
from checks import *

class Tickets(commands.Cog, name='Tickets'):
    def __init__(self, bot):
        self.bot = bot

    async def alt(self, ctx, user: discord.Member):
        await ctx.send('e')

    @commands.command(name='')
    async def closeticket(self, ctx):
        pass

    @commands.command()
    @commands.is_owner()
    async def send_ticket(self, ctx):
        view = ChoseSupport(ctx)

        embed = discord.Embed(title='Support Ticket', description='Click the button you need support with, please do not click for the fun of it', color=0xaaeeaa)
        embed.add_field(name='VPN', value='Click if you have spotted a user using a VPN', inline=False)
        embed.add_field(name='ALT', value='Click to report someone using an alt or avoiding a ban using an alt', inline=False)
        embed.add_field(name='Scammer', value='Click to report someone scamming or a possible scammer', inline=False)
        embed.add_field(name='Other', value='Click if there is something else you need help with or you need to report', inline=False)
        await self.bot.get_channel(827607579731558471).send(embed=embed, view=view)

        if view.value == 0:
            await ctx.send('e')

        if view.value == 1:
            await ctx.send('ee')

        if view.value == 2:
            await ctx.send('eee')

        if view.value == 3:
            await ctx.send('eeee')

def setup(bot):
    bot.add_cog(Tickets(bot))