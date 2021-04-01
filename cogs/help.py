import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###Help###
    @commands.command()
    async def help(self, ctx, cog=None):
        if cog is None:
            help_embed = discord.Embed(title='Brunis Utilities', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Donations', value='Track how much someone has donated in the server', inline=False)
            help_embed.add_field(name='Coming Soon...', value='Coming Soon...', inline=False)
            await ctx.send(embed=help_embed)

        if cog == 'dono' or cog == 'donation':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='See how much someone has doneted in the server```b!dono <@member / id>```', inline=False)
            help_embed.add_field(name='Dono_add', value='Add to someones donations(must have the giveaway manager or heist manger role)```b!da <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Dono_remove', value='Removes from someones donation amount```b!dr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Dono_set(coming soon)', value='Sets the amount donated to a certain member```b!ds <@member /id> <amount(int)>```', inline=False)
            await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))