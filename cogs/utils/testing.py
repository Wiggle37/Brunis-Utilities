import aiohttp
import discord
from discord.ext import commands

from typing import List

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    @commands.command()
    async def m(self, ctx: commands.Context):
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send('Do you want pussy??? its pretty good', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            await ctx.send('timed out...')
        elif view.value:
            async with self.session.get('https://some-random-api.ml/img/cat') as response:
                dogjson = await response.json()
            embed = discord.Embed(title="Kitty Cat 🐈!", color=discord.Color.purple())
            embed.set_image(url=dogjson['link'])
            await ctx.send(embed=embed)

        else:
            print('ok no pussy for you ig')

def setup(bot):
    bot.add_cog(Testing(bot))