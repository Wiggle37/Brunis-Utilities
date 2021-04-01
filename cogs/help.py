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
            help_embed.add_field(name='Giveaway Donation', value='Track how much someone has donated for giveaways', inline=False)
            help_embed.add_field(name='Heist Donations', value='Track how much someone has donated for heists', inline=False)
            help_embed.add_field(name='Event Donations', value='Track how much someone has donated for events', inline=False)
            await ctx.send(embed=help_embed)

        if cog == 'giveaway' or cog == 'gaw':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='See how much someone has doneted in the server```b!d <@member / id>```', inline=False)
            help_embed.add_field(name='Giveaway Dono Add', value='Add to someones donations(must have the giveaway manager or heist manger role)```b!gda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Giveaway Dono Remove', value='Removes from someones donation amount```b!gdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Giveaway Dono Reset', value='Restes the donation amount for the specified number```b!gdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        if cog == 'heist':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='See how much someone has doneted in the server```b!d <@member / id>```', inline=False)
            help_embed.add_field(name='Heist Dono Add', value='Add to someones donations(must have the giveaway manager or heist manger role)```b!hda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Heist Dono Remove', value='Removes from someones donation amount```b!hdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Heist Dono Reset', value='Restes the donation amount for the specified number```b!hdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)
        
        if cog == 'event':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='See how much someone has doneted in the server```b!d <@member / id>```', inline=False)
            help_embed.add_field(name='Event Dono Add', value='Add to someones donations(must have the giveaway manager or heist manger role)```b!eda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Event Dono Remove', value='Removes from someones donation amount```b!edr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Event Dono Reset', value='Restes the donation amount for the specified number```b!edrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        if cog == 'settings' or cog == 'config':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Coming Soon!...', value=None)
            await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))