import discord
import traceback
from discord.ext import commands
from discord.utils import get

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fire(self, ctx):
        await ctx.send('fire pog')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Do note that this will alwaus fire regardless if the command has a cog handler or local handler
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"The command `{ctx.message.content}` is not found")

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"The member provided was not found")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You are missing the `{error.param.name}` argument in the command\n```b!{ctx.command} {ctx.command.signature}```")

        if isinstance(error, commands.BotMissingPermissions):
            wiggle = self.bot.get_user(824010269071507536)
            return await wiggle.send(f"Alert! The bot is missing permissions in {ctx.channel.mention} for `{ctx.command}` please get this fixed right away")

        if isinstance(error, commands.NotOwner):
            return await ctx.send("You need to be the owner of the bot to run this command")

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f"The role provided was not found")

        if isinstance(error, commands.MissingAnyRole):
            # allows owners to bypass checking for roles
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()
            
            role_name = [discord.utils.get(ctx.guild.roles, id = id).name for id in error.missing_roles]
            return await ctx.send(f'You are missing one of the following roles: `{", ".join(role_name)}`')

        if isinstance(error, commands.MissingPermissions):
            pass

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