import discord
from discord.ext import commands
from discord.ext.commands.converter import clean_content

class HelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '`{0.clean_prefix}{1.qualified_name} {1.signature}`'.format(self, command)

class Help(commands.Cog):
    def __init__(self, client):
        self._original_help_command = client.help_command
        client.help_command = HelpCommand()
        client.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(client):
    client.add_cog(Help(client))
    client.get_command('help').hidden = True