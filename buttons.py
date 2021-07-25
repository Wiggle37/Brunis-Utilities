import discord

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def interaction_check(self, interaction: discord.Integration) -> bool:
        return await super().interaction_check(interaction)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()

class ChosePremium(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.interaction_check(interaction)
        self.value = None

    @discord.ui.button(label='Premium', style=discord.ButtonStyle.green)
    async def premium(self, button: discord.ui.Button, interaction: discord.Integration):
        self.value = True
        self.stop()

    @discord.ui.button(label='Not Premium', style=discord.ButtonStyle.red)
    async def nopremium(self, button: discord.ui.Button, interaction: discord.Integration):
        self.value = False
        self.stop()