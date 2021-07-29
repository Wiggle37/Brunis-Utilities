import discord

class Confirm(discord.ui.View):
    def __init__(self, invoked_user_id):
        super().__init__()
        self.value = None
        self.invoked_user_id = invoked_user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.invoked_user_id

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()

class ChoseLockdown(discord.ui.View):
    def __init__(self, invoked_user_id):
        super().__init__()
        self.value = None
        self.invoked_user_id = invoked_user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.invoked_user_id

    @discord.ui.button(label='Dank Memer Lockdown', style=discord.ButtonStyle.green)
    async def dank(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('This will lock down channels for dank memer, the rest of the server will be unaffected', ephemeral=True)
        self.value = 0
        self.stop()

    @discord.ui.button(label='Staff Lockdown', style=discord.ButtonStyle.grey)
    async def staff(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('This will lockdown all public channels, staff channels and private channels will be unaffected', ephemeral=True)
        self.value = 1
        self.stop()

    @discord.ui.button(label='Secure Lockdown', style=discord.ButtonStyle.red)
    async def secure(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('All channels of the server will be locked down until prompted to unlockdown, **NO MEMBERS WILL BE ABLE TO JOIN THE SERVER DURING THIS TIME**, however staff channels and private channels will be affected', ephemeral=True)
        self.value = 2
        self.stop()

class ChosePremium(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Premium', style=discord.ButtonStyle.green)
    async def premium(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='Not Premium', style=discord.ButtonStyle.red)
    async def nopremium(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()