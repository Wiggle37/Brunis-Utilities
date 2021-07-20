import discord

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    def check_author(self, ctx, interaction: discord.Integration):
        return ctx.author == interaction.author

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()