import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(784492058756251669, 784527745539375164, 785202756641619999, 788738308879941633) #Admin, Mod, Bruni, Bot Dev
    async def addrole(self, ctx, member: discord.Member=None, role:discord.Role=None):
        client = self.client
        await member.add_roles(role)

def setup(client):
    client.add_cog(Admin(client))