import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###Help###
    @commands.command(aliases=['cmds', 'commands'])
    async def help(self, ctx, cog=None):
        #Main Help
        if cog is None:
            help_embed = discord.Embed(title='Brunis Utilities', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/827369094776356905/828079209623584818/dankmerchants.gif')
            help_embed.add_field(name='__Donations__', value='To track donations for members', inline=False)
            help_embed.add_field(name='__Giveaway Donation__', value='Track how much someone has donated for giveaways', inline=False)
            help_embed.add_field(name='__Heist Donations__', value='Track how much someone has donated for heists', inline=False)
            help_embed.add_field(name='__Event Donations__', value='Track how much someone has donated for events', inline=False)
            help_embed.add_field(name='__Special Event Donations__', value='Track how much someone has donated for special events', inline=False)
            help_embed.add_field(name='__Money Donations__', value='Track how much someone has donated in real money', inline=False)
            help_embed.add_field(name='__Economy__', value='The servers economy system', inline=False)
            help_embed.add_field(name='__Utility__', value='Utility commands to make life much more easier', inline=False)
            help_embed.add_field(name='__Info__', value='Commands that show info about the server', inline=False)
            await ctx.send(embed=help_embed)

        #Donation Help
        if cog == 'dono' or cog == 'donation':
            help_embed = discord.Embed(title='Donations', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Dono', value='Check your own donation amount for the server```b!dono```')
            help_embed.add_field(name='Init', value='Run this command if it wont let you check your donation amount```b!init```', inline=False)
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
            help_embed.add_field(name='Bug', value='Report a bot bug to Wiggle```b!bug <Wiggles ID> <bug>```', inline=False)
            help_embed.add_field(name='Timer', value='Make a timer```b!count <time(max: 1000)>```', inline=False)
            await ctx.send(embed=help_embed)

        #Economy Help
        if cog == 'econ' or cog == 'economy':
            help_embed = discord.Embed(title='Economy', description='The servers economy system to get some perks\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Balance', value='Check you or someones balance```b!balance```', inline=False)
            help_embed.add_field(name='Inventory', value='Check your inventory```b!inventory <page>```', inline=False)
            help_embed.add_field(name='Beg', value='Be annoying and beg for someone to give you money```b!beg```')
            help_embed.add_field(name='Bet', value='Bet some money and maybe win some more!```b!bet <amount>```')
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
            help_embed.add_field(name='Dank Merchants Exclusive Roles', value='The lsit of exclusive roles in the serber```b!eroles```', inline=False)
            help_embed.add_field(name='Dank Merchants Donor Perks', value='All of the donor perks for the server```b!donoperks```', inline=False)
            help_embed.add_field(name='Dank Merchants Invite Perks', value='All the perks you can get for geting invites in the server```b!invperks```', inline=False)
            help_embed.add_field(name='Dank Merchants Booster Perks', value='Booster perks for the server```b!booster```', inline=False)
            await ctx.send(embed=help_embed)

        #Admin Help
        if cog == 'admin':
            help_embed = discord.Embed(title='Admin', description='Commands only admin can use\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='Coming Soon', value='Coming soon', inline=False)
            await ctx.send(embed=help_embed)

def setup(client):
    client.add_cog(Help(client))