from discord.ext import commands
import textwrap
from contextlib import redirect_stdout
from pathlib import Path
import traceback
import io
import os

class admin(commands.Cog, name = "Admin"):
    def __init__(self, bot):
        self.bot = bot

    def is_valid_ext(self, ext_name: str) -> bool:
        # only looks in files in a directory called cogs
        py_paths = Path("cogs").glob('**/*.py')

        # checks if the name provided is a valid name
        for path in py_paths:

            # irregardless of captialisation
            if ext_name.lower() == path.name[:-3].lower():

                # returns a string of the path instead of the instance
                return str(path)
        
        return None

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension: str):
        """gets a valid path if the extension exists, otherwise it's None"""
        ext = self.is_valid_ext(extension)

        if ext is None:
            return await ctx.send("That wasn't a valid extension")

        # prepares the extension for loading
        ext = ext.replace("\\", ".")[:-3]

        # loads the extension
        self.bot.load_extension(ext)
        await ctx.send(f'Loaded **{ext}**')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        """gets a valid path if the extension exists, otherwise it's None"""
        ext = self.is_valid_ext(extension)

        if ext is None:
            return await ctx.send("That wasn't a valid extension")

        # prepares the extension for unloading
        ext = ext.replace("\\", ".")[:-3]

        # unloads the extension
        self.bot.unload_extension(ext)
        await ctx.send(f'Unloaded **{ext}**')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        """gets a valid path if the extension exists, otherwise it's None"""
        ext = self.is_valid_ext(extension)
        
        if ext is None:
            return await ctx.send("That wasn't a valid extension")

        # prepares the extension for reloading
        ext = ext.replace("\\", ".")[:-3]

        self.bot.unload_extension(ext)
        self.bot.load_extension(ext)
        await ctx.send(f'Reloaded **{ext}**')

    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx: commands.Context):
        for folder in [f for f in os.listdir("./cogs") if f != "__pycache__"]:
            if folder.endswith(".py"):
                self.bot.unload_extension(f'cogs.{folder[:-3]}')
                self.bot.load_extension(f"cogs.{folder[:-3]}")
            else:
                for file in [f for f in os.listdir(f"./cogs/{folder}") if f != "__pycache__"]:
                    self.bot.unload_extension(f"cogs.{folder}.{file[:-3]}")
                    self.bot.load_extension(f"cogs.{folder}.{file[:-3]}")

        await ctx.send('Refreshed the whole bot')

    
    async def send_code(self, ctx, line):
        """Ensures that outputs do not exceed 2000 messages to throw an error
        Does this by splitting the output into exactly 2000 messages each"""
        lines = [line[i:i+1990] for i in range(0, len(line), 1990)]

        for l in lines:
            await ctx.send(f"```py\n{l}\n```")
        
    
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    @commands.is_owner()
    @commands.command()
    async def eval(self, ctx, *, body):        

        # defining variables we can use in the eval function
        env = {
            "self": self,
            "ctx": ctx,
        }

        # adding globals to the eval function
        env.update(globals())
        body = self.cleanup_code(body)

        # for wiggle's weird keyboard
        body = body.replace("“", "\"").replace("”", "\"")

        # two spaces per indent
        # we use an async def function to preserve awaiting inside the eval function
        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"

        try:
            # this is the part where the code is compiled
            exec(to_compile, env)
            # if any exception is thrown (Syntax Errors, etc), send back the error
        except Exception as e:
            return await self.send_code(ctx, f"{e.__class__.__name__}: {e}")
        
        # since we have compiled the code, it would be in our local variables
        func = env['func']

        # we're going to print the result into stdout and get any results from there
        stdout = io.StringIO()
        try:
            with redirect_stdout(stdout):
            # here, we run the code              
                ret = await func()

        except Exception as e:
            value = stdout.getvalue()
            await self.send_code(ctx, f"{value}{traceback.format_exc()}")
        
        else:
            value = stdout.getvalue()
            await ctx.message.add_reaction('\u2705')

            # if nothing has been returned but something has been printed, return the printed value
            if ret is None:
                if value:
                    await self.send_code(ctx, value)
            
            # else we send the returned value
            else:
                await self.send_code(ctx, f'{value}{ret}')

def setup(bot):
    bot.add_cog(admin(bot))