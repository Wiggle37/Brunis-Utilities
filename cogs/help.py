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
            help_embed.add_field(name='Info', value='Some commands that show info about the server', inline=False)
            help_embed.set_footer(text='If you have any questions or bugs please DM Wiggle and we will get back to you as soon as possible!')
            await ctx.send(embed=help_embed)

        #Donation Help
        if cog == 'dono' or cog == 'donation':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='Check your own donation amount for the server```b!dono```')
            help_embed.add_field(name='Dono', value='Check someones donation amount for the server(shows all donated amounts)```b!dono <@member / id>```', inline=False)
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

        #Special Event Help
        if cog == 'special':
            help_embed = discord.Embed(title='Special Event Donations', description='Must have Event Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Special Event Dono Add', value='Add to someones donations```b!sda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Special Event Dono Remove', value='Removes from someones donation amount```b!sdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Special Event Dono Reset', value='Restes the donation amount for the specified number```b!sdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        #Money Help
        if cog == 'money':
            help_embed = discord.Embed(title='Money Donations', description='Must have Event Manager role\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Money Dono Add', value='Add to someones donations```b!mda <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Money Dono Remove', value='Removes from someones donation amount```b!mdr <@member / id> <amount(int)>```', inline=False)
            help_embed.add_field(name='Money Dono Reset', value='Restes the donation amount for the specified number```b!mdrs <@member /id>```', inline=False)
            await ctx.send(embed=help_embed)

        #Utility Help
        if cog == 'utility' or cog == 'utils' or cog == 'util':
            help_embed = discord.Embed(title='Utility', description='Commands that will probally be useful\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='<a:loading:802974837395292200>Coming Soon...', value='<a:loading:802974837395292200>Coming soon...')
            await ctx.send(embed=help_embed)

        #Info Help
        if cog == 'info':
            help_embed = discord.Embed(title='Info', description='A list of commands for info to quickly display\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dank Merchants Rules', value='The rules of Dank Merchants to quickly display```b!rules```', inline=False)
            help_embed.add_field(name='Dank Memer Rules', value='The rules of Dank Memer to quickly display```b!dankrules```', inline=False)
            help_embed.add_field(name='Dank Merchants Warning Policy', value='The warning policy of Dank Merchants```b!warnp```', inline=False)
            help_embed.add_field(name='Dank Merchants Trading Rules', value='The Dank Merchants trading rules```b!traderules```', inline=False)
            help_embed.add_field(name='Dank Merchants Giveaway Rules', value='The giveaway rules for Dank Merchants```b!gawrules```', inline=False)
            help_embed.add_field(name='Dank Merchants Special Roles', value='A list of special roles you can get```b!specroles```', inline=False)
            help_embed.add_field(name='Dank Merchants Exlusive Roles', value='The lsit of exlusive roles in the serber```b!eroles```', inline=False)
            help_embed.add_field(name='Dank Merchants Donor Perks', value='All of the donor perks for the server```b!donoperks```', inline=False)
            help_embed.add_field(name='Dank Merchants Invite Perks', value='All the perks you can get for geting invites in the server```b!invperks```', inline=False)
            help_embed.add_field(name='Dank Merchants Booster Perks', value='Booster perks for the server```b!booster```', inline=False)
            await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))