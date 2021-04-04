import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    #on Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        client = self.client

        await client.get_channel(784491141022220312).send(f'{member.mention}')
        join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
        join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for some info about how to get certain thing in the server and <#784547669619507201> for some self roles!')
        join_embed.add_field(name=f'__**User Info:**__', value=f'Date created: {member.created_at}\nUser ID: {member.id}', inline=False)
        await client.get_channel(784491141022220312).send(embed=join_embed)

def setup(client):
    client.add_cog(Events(client))