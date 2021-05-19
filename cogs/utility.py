import discord
from discord.ext import commands
import asyncio
from discord.ext.commands.core import command

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Timer
    @commands.command()
    async def count(self, ctx, number: int):
        client = self.client
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

    #Giveaway announcement
    @commands.command()
    @commands.has_role(785198646731604008)
    async def gaw(self, ctx, sponser: discord.Member=None, *, msg='No message provided'):
        if sponser == None:
            await ctx.send('You have to provide a sponser', delete_after=3)

        else:
            await ctx.message.delete()
            embed = discord.Embed(title=f'Giveaway Donated By {sponser}!', description=f'Message: {msg}', color=0x00ff00)
            embed.add_field(name='More info:', value=f'- Make sure to thank {sponser.mention} in <#784491141022220312>\n- Go to <#785154861922254848> to donate for giveaways\n- Go to <#818269054103978004> to donate for heists')
            embed.set_thumbnail(url='https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/video/uh59Wh0/stacks-of-money-with-coins-cartoon-illustration-hand-drawn-animation-transparent-cartoon-illustration-hand-drawn-animation-transparent_s289_zlf_thumbnail-1080_07.png')
            await ctx.send('<@&785930653665067038>', embed=embed)

def setup(client):
    client.add_cog(Utility(client))