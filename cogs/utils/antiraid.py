import discord
from discord.ext import commands

import json

from config import *

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add Staff
    @commands.command()
    @commands.is_owner()
    async def add_staff(self, ctx, members: commands.Greedy[discord.Member]):
        with open('config.json', 'w') as file:
            for staff in members:
                if staff.id not in CONFIG["settings"]["anti_raid"]["whitelisted_members"]:
                    CONFIG["settings"]["anti_raid"]["whitelisted_members"] += [staff.id]
                else:
                    continue
            json.dump(CONFIG, file, indent=4)

        await ctx.send(f'Added **{len(members)}** to the whitelisted anitraid whitelisted staff list')

    # Remove Staff
    @commands.command()
    @commands.is_owner()
    async def remove_staff(self, ctx, members: discord.Member):
        index = 0
        with open('config.json', 'w') as file:
            for staff in members:
                if staff.id in CONFIG["settings"]["anti_raid"]["whitelisted_members"]:
                    for user in CONFIG["settings"]["anti_raid"]["whitelisted_members"]:
                        if user == staff.id:
                            del CONFIG["settings"]["anti_raid"]["whitelisted_members"][index]
                        index += 1
                else:
                    continue
            json.dump(CONFIG, file, indent=4)

        await ctx.send(f'Removed **{len(members)}** from the whitelisted staff list')

    # Staff List
    @commands.command()
    async def staff_list(self, ctx):
        staff = ''
        for staffs in CONFIG["settings"]["anti_raid"]["whitelisted_members"]:
            staff_ = self.bot.get_guild(784491141022220309).get_member(staffs)
            staff += f'{staff_.name}({staff_.id})\n'

        await ctx.send(f'```{staff}```')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        merchants = self.bot.get_guild(784491141022220309)
        member = merchants.get_member(after._user.id)

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

        role_objs = []
        for role in staff_roles_ids:
            role_ = discord.utils.get(merchants.roles, id=role)
            role_objs.append(role_)

        for role in after.roles:
            if role in role_objs and member.id not in CONFIG["settings"]["anti_raid"]["whitelisted_members"] and not member.bot:
                await member.remove_roles(role)
                await self.bot.get_channel(863178240680394793).send(f'**{after._user}** has been granted a staff role. The role given to **{after._user}** was `{role}`\nThis role was removed, if you think this is a mistake please contact wiggle to get it added to the whitelisted staff members')

    # Save Backup
    @commands.command()
    async def backup(self, ctx):
        pass

def setup(bot):
    bot.add_cog(AntiRaid(bot))