import discord
from discord.ext import commands

import traceback

from config import *

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dank_merchants = self.bot.get_guild(CONFIG["info"]["ids"]["merchants_id"])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)

        # - Check Fail - #
        if isinstance(error, commands.CheckFailure):
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()

        # - Command On Cooldown Errors - #
        if isinstance(error, commands.CommandOnCooldown):
            return ctx.send(f"This command is on cooldown for another {error.cooldown}")

        # - Extenstion Errors - #
        if isinstance(error, commands.ExtensionAlreadyLoaded):
            return await ctx.send("This extenstion is already loaded")

        if isinstance(error, commands.ExtensionNotLoaded):
            return await ctx.send("This extenstion is not loaded")

        if isinstance(error, commands.ExtensionNotFound):
            return await ctx.send("The provided extension was not found")

        # - Disabled Command - #
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send("This command is currently disabled")

        # - Not Found Errors - #
        if isinstance(error, commands.MessageNotFound):
            return await ctx.send(f"The message `{error.argument}` was not found")

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f'The role `{error.argument}` was not found')

        if isinstance(error, commands.ChannelNotFound):
            return await ctx.send(f"The channel `{error.argument}` was not found")

        if isinstance(error, commands.EmojiNotFound):
            return await ctx.send(f"{error.args[0]}")

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"{error.args[0]}")

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"The member provided was not found")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You are missing the `{error.param.name}` argument in the command\n```b!{ctx.command} {ctx.command.signature}```")

        # - Permission Errors - #
        if isinstance(error, discord.errors.Forbidden):
            return await ctx.author.send(f'The bot does not have to correct permissions in this channel please contact a staff member to get perms fixed in {ctx.channel.mention}')

        if isinstance(error, commands.NotOwner):
            return await ctx.send("You need to be the owner of the bot to run this command")

        if isinstance(error, commands.MissingAnyRole):
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()
            
            role_name = [discord.utils.get(self.dank_merchants.roles, id = id).name for id in error.missing_roles]
            return await ctx.send(f"You are missing one of the following roles: `{', '.join(role_name)}`")
        if isinstance(error, commands.MissingRole):
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()

            return await ctx.send(f"You are missing the required role to run this command: `{error.missing_role}`")

        if isinstance(error, commands.MissingPermissions):
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()

            return await ctx.send(f'You are missing the following permission to run this command: `{error.missing_permissions}`')

        # if none of the above we send to a debug channel
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        debug = self.bot.get_channel(CONFIG["info"]["ids"]["debugChannel_id"])
        
        # checking if there's an existing webhook to use
        existing_webhooks = await debug.webhooks()
        
        if existing_webhooks == []:
            debug_webhook = await debug.create_webhook(name = "Bruni's Utilities Error Log", avatar = await ctx.me.avatar.read())
        else:
            debug_webhook = existing_webhooks[0]
        
        # splits the value into strings less than 4096 chars, in case the tb is long
        tb_split = [tb[i:i+4086] for i in range(0, len(tb), 4086)]
        embed_list = [discord.Embed(description = f"```py\n{tb}\n```") for tb in tb_split]
        await debug_webhook.send(embeds = embed_list)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
