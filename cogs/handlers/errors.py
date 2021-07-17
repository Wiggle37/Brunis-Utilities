import discord
from discord.ext import commands
import traceback

from config import *

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dank_merchants = self.bot.get_guild(CONFIG["config"]["info"]["ids"]["merchants_id"])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        # - Check Fail - #
        if isinstance(error, commands.CheckFailure):
            return

        # - Command On Cooldown Errors - #
        if isinstance(error, commands.CommandOnCooldown):
            return ctx.send('This command is on cooldown, chill out')

        # - Disabled Command - #
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send('This command is currently disabled')

        # - Not Found Errors - #
        if isinstance(error, commands.MessageNotFound):
            return await ctx.send('The provied message was not found')

        if isinstance(error, commands.ChannelNotFound):
            return await ctx.send('The provided channel was not found')

        if isinstance(error, commands.ExtensionNotFound):
            return await ctx.send('The provided cog was not found')

        if isinstance(error, commands.EmojiNotFound):
            return await ctx.send('The emoji provided was not found')

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"The command `{ctx.message.content}` is not found")

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"The member provided was not found")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You are missing the `{error.param.name}` argument in the command\n```b!{ctx.command} {ctx.command.signature}```")

        # - Permission Errors - #
        if isinstance(error, commands.NotOwner):
            return await ctx.send("You need to be the owner of the bot to run this command")

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f"The role provided was not found")

        if isinstance(error, commands.MissingAnyRole):
            if ctx.author.id in self.bot.owner_ids:
                await ctx.send('Your command was reinvoked because you are a bot owner.')
                return await ctx.reinvoke()
            
            role_name = [discord.utils.get(self.dank_merchants.roles, id = id).name for id in error.missing_roles]
            return await ctx.send(f'You are missing one of the following roles: `{", ".join(role_name)}`')

        if isinstance(error, commands.MissingPermissions):
            if ctx.author.id in self.bot.owner_ids:
                await ctx.send('Your command was reinvoked because you are a bot owner.')
                return await ctx.reinvoke()

            return await ctx.send(f'You are missing the following permission to run this command: `{error.missing_perms}`')



        # if none of the above we send to a debug channel
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        debug = self.bot.get_channel(844759955815006222)
        # splits the value into strings less than 2000 chars, in case the tb is long
        tb_split = [tb[i:i+1990] for i in range(0, len(tb), 1990)]
        # sends each one
        for info in tb_split:
            await debug.send(f"```py\n{info}\n```")    

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))