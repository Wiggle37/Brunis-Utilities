import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Announce
    @commands.command()
    @commands.is_owner()
    async def announce(self, ctx, *, msg):
        client = self.client

        await client.get_channel(827293945003376650).send(msg)
        await client.get_channel(827293945003376650).send(f'\nMSG sent by: **{ctx.message.author}**')
        await ctx.send('Announcement sent to <#827293945003376650>')

    @announce.error
    async def announce_error(self, ctx, error):
        await ctx.send('Only Wiggle can use this command')

    #Suport
    @commands.command()
    async def sup(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title='__***Dank Merchants Support***__', description='Have a question? Got scammed? Reporting a member or have a general question about anything server related? Ask away! You are more than welcome to speak here.\n\nBut before you ask though, we recommend you to read <#787343840108478474> and <#787390795182506005> as they both contain valuable information about this server.', color=0x00ff00)
        await ctx.send(embed=embed)

        await ctx.send('If you need help ping or dm <@765322777329664089> for support and Ill respond as soon as I can')

    

def setup(client):
    client.add_cog(Owner(client))