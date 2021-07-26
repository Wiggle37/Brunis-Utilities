import discord
from discord.ext import commands

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        merchants = self.bot.get_guild(784491141022220309)

        staff_roles_ids = [
            802939606671949866, # helper
            802939607561535519, # senior helper
            784527745539375164, # moderator
            789642191583838208, # senior moderator
            789642191521316884, # head moderator
            784492058756251669, # admin
            817280207408070677, # head admin
            784499226230784000  # bots
        ]

        whitelisted_staff = [
            497017441591885824, # Aiiiden
            656565295586082828, # Sea
            710656296445018143, # Ethereal
            710656296445018143, # Euph
            840223106345336882, # Dark
            294068906132242432, # Rach
            579393034761011200, # Vogl
            654688268138577931, # Awesome
            695353371535736944, # q13x
            761304458206249000, # Neon
            716525960643739798, # Dukie
            759774736279404614, # Thean
            701713045574909984, # Amercy
            738796323872047204, # Bug
            691798464107118622, # Copi
            732627627235606629, # Suhii
            737020572906684556, # Adit
            824010269071507536  # Wiggle
        ]

        member = merchants.get_member(after._user.id)

        role_objs = []
        for role in staff_roles_ids:
            role_ = discord.utils.get(merchants.roles, id=role)
            role_objs.append(role_)

        for role in after.roles:
            if role in role_objs and member.id not in whitelisted_staff:
                await member.remove_roles(role)
                await self.bot.get_channel(863178240680394793).send(f'**{after._user}** has been granted a staff role!!! the role was removed right away')

def setup(bot):
    bot.add_cog(Testing(bot))