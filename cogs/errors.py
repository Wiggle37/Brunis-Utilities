from inspect import Parameter
from typing import Awaitable
import discord
import traceback
import sys
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound, MissingRequiredArgument

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f'The command `{ctx.message.content}` is not found')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f'That member is not found')

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'You are missing the `{error.param.name}` argument in the `{ctx.command}` command\n```b!{ctx.command} {ctx.command.signature}```')

        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f'The bot is missing some permissions for this command to be run please contact wiggle so he can get this figured out')

        if isinstance(error, commands.MissingRole):
            return await ctx.send(f'You are missing one or more roles to run this command')

        if isinstance(error , commands.MissingPermissions):
            return await ctx.send(f'You are lacking some permissions to run this command')

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f'The role provided was not found')

        if isinstance(error, commands.BadArgument):
            pass

        if isinstance(error, commands.CommandOnCooldown):
            pass

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))