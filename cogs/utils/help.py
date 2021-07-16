import discord
from discord.ext import commands

from datetime import datetime

from discord.ext.commands.core import Command

from config import *

class bruniUtilsHelp(commands.HelpCommand):    
    async def send_bot_help(self, mapping):
        ctx = self.context

        help = discord.Embed(title = "Bruni's Utilities", description = "All commands for the bot", colour = discord.Color.purple())
        ignored_cogs = [
            'CommandErrorHandler',
            'Events',
            'Heist Starter',
            'Sticky'
        ]
        
        for cog in mapping:
            if cog is None or cog.qualified_name in ignored_cogs:
                continue

            help.add_field(name = cog.qualified_name.capitalize(), value = f"{cog.description}\n`{self.clean_prefix}help {cog.qualified_name}`")
        
        help.set_thumbnail(url='https://cdn.discordapp.com/avatars/852670742419603467/e39038e6e8733b14445e99fc2038e1e7.png?size=1024')
        help.timestamp = datetime.utcnow()
        await ctx.send(embed = help)
    
    async def send_cog_help(self, cog):
        ctx = self.context
        cog_help = discord.Embed(title = f"{cog.qualified_name.capitalize()} Commands", colour = discord.Color.purple())

        # filters hidden commands
        filtered = await self.filter_commands(cog.walk_commands(), sort = True)

        # removes subcommands
        filtered = filter(lambda c: True if c.parent is None else False, filtered)
        
        filtered_display = map(lambda c: f"`{c.qualified_name}`", filtered)

        cog_help.description = ", ".join(filtered_display)
        cog_help.set_footer(text = f"Use {self.clean_prefix} before each command!")

        cog_help.set_thumbnail(url='https://cdn.discordapp.com/avatars/852670742419603467/e39038e6e8733b14445e99fc2038e1e7.png?size=1024')
        cog_help.timestamp = datetime.utcnow()
        await ctx.send(embed = cog_help)
    
    async def send_group_help(self, group):
        # this works since Group is a subclass of Command
        return await self.send_command_help(group)
    
    def get_command_signature(self, command):
        return f"```{self.clean_prefix}{command.qualified_name} {command.signature}```"

    async def command_callback(self, ctx, *, command = None):
        if command is not None:
            command = command.lower()
        return await super().command_callback(ctx, command=command)

    async def send_command_help(self, command):
        ctx = self.context

        command_help = discord.Embed(title = f"{self.clean_prefix}{command.qualified_name} info", color=discord.Color.purple())

        description = "No description provided, but a cool command anyway!"
        if command.description != "":
            description = command.description
        command_help.add_field(name = "Description:", value = description, inline = False)
        command_help.add_field(name = "Usage:", value = self.get_command_signature(command), inline = False)

        aliases = ", ".join(command.aliases)
        if len(command.aliases) == 0:
            aliases = command.qualified_name
        command_help.add_field(name = "Aliases:", value = aliases, inline = False)

        command_help.set_footer(text = "Usage Syntax: <required> [optional]")

        command_help.set_thumbnail(url='https://cdn.discordapp.com/avatars/852670742419603467/e39038e6e8733b14445e99fc2038e1e7.png?size=1024')
        command_help.timestamp = datetime.utcnow()
        await ctx.send(embed = command_help)

class Help(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
       help_command = bruniUtilsHelp()
       help_command.cog = self
       bot.help_command = help_command

def setup(bot):
    bot.add_cog(Help(bot))