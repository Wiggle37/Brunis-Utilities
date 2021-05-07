import discord
from discord.ext import commands

class Donations(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Bug
    @commands.command()
    async def bug(self, ctx, *, bug=None):
        if bug is None:
            await ctx.send('You have to say the bug it cant just be blank *smh*')

        else:
            embed = discord.Embed(title='__Bug Report__', description=f'A bug has been reported by **{ctx.message.author}(id: {ctx.message.author.id})**', color=0xff0000)
            embed.add_field(name='Bug:', value=f'{bug}')
            await self.client.get_channel(838204133110579230).send(embed=embed)

    #Suggest
    @commands.command()
    async def suggest(self, ctx, *, suggestion=None):
        if suggestion is None:
            await ctx.send('What is your suggestion?')

        else:
            embed = discord.Embed(title='__Suggestion__', description=f'A suggestion has been added by **{ctx.message.author}(id: {ctx.message.author.id})**', color=0x00ff00)
            embed.add_field(name='Suggestion:', value=f'{suggestion}')
            message = await self.client.get_channel(838204401964417064).send(embed=embed)

            await message.add_reaction('✅')
            await message.add_reaction('❌')

def setup(client):
    client.add_cog(Donations(client))