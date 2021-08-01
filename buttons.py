import discord
from discord.enums import ButtonStyle

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
    def __init__(self):
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

class ChoseSupport(discord.ui.View):
    def __init__(self, guild):
        super().__init__(timeout=None)
        self.value = None
        self.guild = guild

    @discord.ui.button(label='❗ Alt', style=discord.ButtonStyle.grey, custom_id='persistent_view:alt')
    async def alt(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket created for reporting an alt', ephemeral=True)
        channel = await self.guild.create_text_channel(name='alt-report-ticket')
        await channel.set_permissions(interaction.user.id, read_messages=True, send_messages=True)
        self.value = 0

    @discord.ui.button(label='❌ VPN', style=discord.ButtonStyle.grey, custom_id='persistent_view:vpn')
    async def vpn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket created for reporting someone using a vpn', ephemeral=True)
        await self.guild.create_text_channel(name='vpn-report-ticket')
        self.value = 1

    @discord.ui.button(label='⚖ Scammer', style=discord.ButtonStyle.grey, custom_id='persistent_view:scammer')
    async def scammer(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket created for reporting a scammer', ephemeral=True)
        await self.guild.create_text_channel(name='scam-report-ticket')
        self.value = 2

    @discord.ui.button(label='📥 Other', style=discord.ButtonStyle.grey, custom_id='persistent_view:other')
    async def other(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Ticket created', ephemeral=True)
        await self.guild.create_text_channel(name='support-ticket')
        self.value = 3