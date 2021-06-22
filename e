import discord
from discord.ext import commands
from datetime import datetime

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    #Help
    @commands.command(aliases=['cmds', 'commands'])
    async def help(self, ctx, command=None):
        #Main Help
        if command is None:
            help_embed = discord.Embed(title='Brunis Utilities', description='All of the categorys', color=0x00ff00)
            help_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/827369094776356905/828079209623584818/dankmerchants.gif')
            help_embed.add_field(name='__Donations__', value='To track donations for members', inline=False)
            help_embed.add_field(name='__Economy__', value='The servers economy system', inline=False)
            help_embed.add_field(name='__Utility__', value='Utility commands to make life much more easier', inline=False)
            help_embed.add_field(name='__Info__', value='Commands that show info about the server', inline=False)
            await ctx.send(embed=help_embed)

        #Donation Help
        if command == 'dono' or command == 'donation' or command == 'donations':
            help_embed = discord.Embed(title='Donations', description='dono', color=0x00ff00)
            help_embed.add_field(name='__**Basic:**__', value='`b!dono` ➞ Check how much you have donated\n`b!init` ➞ Add you self to the database')
            help_embed.add_field(name='__**Giveaway Donations:**__', value='`b!gda <@member / id> <amount>` ➞ Add to someones giveaway donations\n`b!gdr <@member / id> <amount>` ➞ Remove from someones giveaway donations\n`b!gds <@member / id> <amount>` ➞ Set someones donations\n`b!gdrs <@member / id>` ➞ Reset someones giveaway donations', inline=False)
            help_embed.add_field(name='__**Heist Donations:**__', value='`b!hda <@member / id> <amount>` ➞ Add to someones heist donations\n`b!hdr <@member / id> <amount>` ➞ Remove from someones heist donations\n`b!hds <@member / id> <amount>` ➞ Set someones heist donations\n`b!hdrs <@member / id>` ➞ Reset someones heist donations', inline=False)
            help_embed.add_field(name='__**Event Donations:**__', value='`b!eda <@member / id> <amount>` ➞ Add to someones event donations\n`b!edr <@member / id> <amount>` ➞ Remove from someones event donations\n`b!eds <@member / id> <amount>` ➞ Set someones event donations\n`b!edrs <@member / id>` ➞ Reset someones event donations', inline=False)
            help_embed.add_field(name='__**Special Event Donations:**__', value='`b!sda <@member / id> amount` ➞ Add to someones special event donations\n`b!sdr <@member / id> <amount>` ➞ Remove from someones special event donations\n`b!sds <@member / id> <amount>` ➞ Set someones special event donations\n`b!sdrs <@member / id>` ➞ Reset someones special event donations', inline=False)
            help_embed.add_field(name='__**Money Donations:**__', value='`b!mda <@member / id> <amount>` ➞ Add to someones money donations\n`b!mdr <@member / id> <amount>` ➞ Remove from someones money donations\n`b!mds <@member / id> <amount>` ➞ Set someones money donations\n`b!mdrs <@member / id>` ➞ Reset someones money donations', inline=False)
            await ctx.send(embed=help_embed)

        #Utility Help
        if command == 'utility' or command == 'utils' or command == 'util':
            help_embed = discord.Embed(title='Utility', description='Commands that will probally be useful', color=0x00ff00)
            help_embed.add_field(name='__**Useful:**__', value='`b!count` ➞ Count to up to 1000', inline=False)
            await ctx.send(embed=help_embed)

        #Economy Help
        if command == 'econ' or command == 'economy':
            help_embed = discord.Embed(title='Economy', description='economy', color=0x00ff00)
            help_embed.add_field(name='__**Basic:**__', value='`b!bal [@member / id]` ➞ Check how much money you have\n`b!inv [page] [member]` ➞ Check what you have in your inventory', inline=False)
            help_embed.add_field(name='__**Money Making:**__', value='`b!beg` ➞ Gives you some money\n`b!bet <amount>` ➞ Risk losing some money but have a chance of winning even more\n`b!work` ➞ Go to work and do some things that could make you some money', inline=False)
            await ctx.send(embed=help_embed)

        #Info Help
        if command == 'info':
            help_embed = discord.Embed(title='Info', description='A list of commands for info to quickly display\n[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='__**Rules:**__', value='`b!dankrules` ➞ The rules of Dank Memer you must follow to not get banned\n`b!rules` ➞ The rules of Dank Merchats you must follow them\n`b!traderules` ➞ The trading rules of Dank Merchants you must follow\n`b!gawrules` ➞ The rules for Dank Merchants giveaways\n`b!warnp` ➞ The warning policy for Dank Merchants', inline=False)
            help_embed.add_field(name='__**Roles:**__', value='`b!specroles` ➞ A list of special roles for Dank Merchats\n`b!eroles` ➞ A list of exclusive roles that are hard to get', inline=False)
            help_embed.add_field(name='__**Perks:**__', value='`b!donoperks` ➞ All of the donor perks for the server\n`b!invperks` ➞ All of the perks to inviting people to the server\n`b!booster` ➞ The perks to boosting the server', inline=False)
            await ctx.send(embed=help_embed)

        #Admin Help
        if command == 'admin':
            help_embed = discord.Embed(title='Admin', description='[Dank Merchants](https://discord.gg/S5sNmzfF9M)', color=0x00ff00)
            help_embed.add_field(name='__**Roles:**__', value='`b!ar <@member / id> <@role / id>` ➞ Give someone a role\n`b!rr <@member / id> <@role / id>` ➞ Remove a role from someone', inline=False)
            help_embed.add_field(name='__**Messages:**__', value='`b!purge <amount>` ➞ Delete up-to 1000 messages', inline=False)
            help_embed.add_field(name='__**Channels:**__', value='`b!lock` ➞ Locks the current channel\n`b!unlock` ➞ Unlocks the current channel')
            await ctx.send(embed=help_embed)
    
    def lowercase(self, arg):
        x = []
        for command in self.client.commands:
            i = (command.name).lower()
            x.append(i)

        return x

    @commands.command()
    async def helps(self, ctx, *, arg=None):
        embed = discord.Embed(title="Bruni's Utilities", description='All commands for the bot', color=discord.Color.purple())
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/852670742419603467/e39038e6e8733b14445e99fc2038e1e7.png?size=1024')
        embed.timestamp = datetime.utcnow()

        if arg is None:
            for cog in self.client.cogs:
                if cog == 'CommandErrorHandler' or cog == 'Heist Starter' or cog == 'Music' or cog == 'Events' or cog == 'Help' or cog == 'Stickys':
                    pass
                else:
                    cog_ = self.client.get_cog(cog)
                    embed.add_field(name=cog_.name, value=f'{cog_.description}', inline=False)
            await ctx.send(embed=embed)

        elif arg.capitalize() is not None and arg in self.client.cogs:
            cog_ = self.client.get_cog(arg)
            commands = cog_.get_commands()

            num = 0
            for command in commands:
                name = commands[num].name
                description = commands[num].description
                if commands[num].description is None:
                    description = '-'

                embed.add_field(name=name, value=description, inline=False)
                num += 1

            await ctx.send(embed=embed)
                
def setup(client):
    client.add_cog(Help(client))