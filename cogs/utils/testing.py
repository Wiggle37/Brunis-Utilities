import aiohttp
import discord
from discord.ext import commands

from typing import List

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def m(self, ctx: commands.Context):
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send('e', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            await ctx.send('timed out...')
        elif view.value:
            pass

        else:
            await ctx.send('e')

def setup(bot):
    bot.add_cog(Testing(bot))