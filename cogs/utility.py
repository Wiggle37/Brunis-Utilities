import discord
from discord.ext import commands

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bug(self, ctx, member: discord.Member, *, msg):
        channel = await member.create_dm()
        
        message = ctx.message
        await message.add_reaction(emoji="✅")

        dm_embed = discord.Embed(title=f'You Have A Bug Report From {ctx.message.author}', description=f'{msg}', color=0x00ff00)
        await channel.send(embed=dm_embed)
        
        await ctx.send(f'Bug report sent to **{member}**')

def setup(client):
    client.add_cog(Utility(client))