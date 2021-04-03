import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###Help###
    @commands.command()
    async def help(self, ctx, cog=None):
        #Main Help
        if cog is None:
            help_embed = discord.Embed(title='Brunis Utilities', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Donations', value='To track donations for members', inline=False)
            help_embed.add_field(name='Giveaway Donation', value='Track how much someone has donated for giveaways', inline=False)
            help_embed.add_field(name='Heist Donations', value='Track how much someone has donated for heists', inline=False)
            help_embed.add_field(name='Event Donations', value='Track how much someone has donated for events', inline=False)
            help_embed.add_field(name='Utility', value='Utility commands to make life much more easier', inline=False)
            help_embed.set_footer(text='If you have any questions or bugs please DM **<@765322777329664089>** and we will get back to you as soon as possible!')
            await ctx.send(embed=help_embed)

        #Donation Help
        if cog == 'dono' or cog == 'donation':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='Check someones donation amount for the server(shows all donated amounts)```b!d <@member / id>```', inline=False)
            await ctx.send(embed=help_embed)

        #Giveaway Help
        if cog == 'giveaway' or cog == 'gaw':
            help_embed = discord.Embed(title='Giveaway Donations', description='Must have Giveaway Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Giveaway Dono Add', value='Add to someones donations```b!gda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Giveaway Dono Remove', value='Removes from someones donation amount```b!gdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Giveaway Dono Reset', value='Restes the donation amount for the specified number```b!gdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        #Heist Help
        if cog == 'heist' or cog == 'heists':
            help_embed = discord.Embed(title='Heist Donations', description='Must have Heist Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Heist Dono Add', value='Add to someones donations```b!hda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Heist Dono Remove', value='Removes from someones donation amount```b!hdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Heist Dono Reset', value='Restes the donation amount for the specified number```b!hdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)
        
        #Event Help
        if cog == 'event' or cog == 'events':
            help_embed = discord.Embed(title='Event Donations', description='Must have Event Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Event Dono Add', value='Add to someones donations```b!eda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Event Dono Remove', value='Removes from someones donation amount```b!edr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Event Dono Reset', value='Restes the donation amount for the specified number```b!edrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        #Utility Help
        if cog == 'utility' or cog == 'utils' or cog == 'util':
            help_embed = discord.Embed(title='Event Donations', description='Must have Event Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Coming Soon...', value='Coming soon')
            await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))