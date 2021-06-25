import discord
import traceback
import sys
from discord.ext import commands

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errors = [
            commands.CommandNotFound,
            commands.MemberNotFound,
            commands.MissingRequiredArgument,
            commands.BotMissingPermissions,
            commands.MissingRole,
            commands.MissingAnyRole,
            commands.MissingPermissions,
            commands.NotOwner,
            commands.RoleNotFound,

        ]
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f'The command `{ctx.message.content}` is not found')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f'That member is not found')

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'You are missing the `{error.param.name}` argument in the `{ctx.command}` command\n```b!{ctx.command} {ctx.command.signature}```')

        if isinstance(error, commands.BotMissingPermissions):
            wiggle = self.client.get_user(824010269071507536)
            return await wiggle.send(f'Alert! The bot is missing permissions in {ctx.channel.mention} for `{ctx.command}` please get this fixed right away')

        if isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingAnyRole):
            return await ctx.send(f'You are missing one or more roles to run this command')

        if isinstance(error , commands.MissingPermissions):
            return await ctx.send(f'You are lacking some permissions to run this command')

        if isinstance(error, commands.NotOwner):
            return await ctx.send('You need to be the owner of the bot to run this command')

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f'The role provided was not found')
        
        if isinstance(error, discord.errors.Forbidden):
            wiggle = self.client.get_user(824010269071507536)
            return await wiggle.send(f'Alert! The bot is missing permissions in {ctx.channel.mention} for `{ctx.command}` please get this fixed right away')
        
        if isinstance(error, commands.BadArgument):
            pass

        if isinstance(error, commands.CommandOnCooldown):
            pass

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))