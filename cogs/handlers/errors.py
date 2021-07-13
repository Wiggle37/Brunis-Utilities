import discord
import traceback
from discord.ext import commands
import io

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _get_req(self, command: commands.Command) -> dict:
        """Gets the required roles/perms required to run a command
        This is done by intentionally causing an error within the predicate
        Tracebacks would then show the locals within said predicate
        
        Note that this function does not differentiate between roles and perms, 
        for that, check get_req_roles and get_req_perms, both of which call this function"""

        try:
            # get the first check
            check = command.checks[0]

            # We will now intentionally cause an error within the check function
            # This will error as ctx is passed as 0
            check(0)

        except Exception as e:
            # Get the last frame of the generator
            *frames, last_frame = traceback.walk_tb(e.__traceback__)

            # Getting the first element to get the trace
            frame = last_frame[0]
            return frame.f_locals
    
    def get_perms_req(self, command: commands.Command) -> dict:
        return self._get_req(command)["perms"]

    def get_roles_req(self, command: commands.Command) -> set:
        return self._get_req(command)["items"]

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Do note that this will alwaus fire regardless if the command has a cog handler or local handler
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        ignored = (commands.BadArgument, commands.CommandOnCooldown, commands.CheckFailure)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"The command `{ctx.message.content}` is not found")

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"The member was not found")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"You are missing the `{error.param.name}` argument in the command\n```b!{ctx.command} {ctx.command.signature}```")

        if isinstance(error, commands.BotMissingPermissions):
            wiggle = self.bot.get_user(824010269071507536)
            return await wiggle.send(f"Alert! The bot is missing permissions in {ctx.channel.mention} for `{ctx.command}` please get this fixed right away")

        if isinstance(error, commands.NotOwner):
            return await ctx.send("You need to be the owner of the bot to run this command")

        if isinstance(error, commands.RoleNotFound):
            return await ctx.send(f"The role provided was not found")


        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            # allows owners to bypass checking for roles
            if ctx.author.id in self.bot.owner_ids:
                return await ctx.reinvoke()

            # gets the role ids required to run the command
            roles_req = self.get_roles_req(ctx.command)

            # gets the names of each role
            role_names = [discord.utils.get(ctx.guild.roles, id = id).name for id in roles_req]

            return await ctx.send(f"You are missing any of these roles to run a command: `{', '.join(role_names)}`")


        if isinstance(error , commands.MissingPermissions):
            # gets the perms required to run the command
            roles_req = self.get_perms_req(ctx.command)

            # formats the perms properly
            perm_names = map(lambda r: r.replace("_", " ").title(), roles_req.keys())

            return await ctx.send(f"You are these permissions to run this command: {', '.join(perm_names)}")

        # else, we send the error to a debug channel

        # we shall print the error straight into stdout and get the tb from there
        stdout = io.StringIO()
        print(f"Ignoring exception in command {ctx.command}:", file = stdout)
        traceback.print_exception(type(error), error, error.__traceback__, file = stdout)
        tb = stdout.getvalue()

        debug = self.bot.get_channel(844759955815006222)

        # splits the value into strings less than 2000 chars, in case the tb is long
        tb_split = [tb[i:i+1990] for i in range(0, len(tb), 1990)]

        # sends each one
        for info in tb_split:
            await debug.send(f"```py\n{info}\n```")    
    

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))