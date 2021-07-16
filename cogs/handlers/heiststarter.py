import discord
from discord.ext import commands
import asyncio

from config import *

class HeistStarter(commands.Cog, name='Heist Starter', command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def get_heist_results(self, invocation_message):
        def check(message):
            return message.author.id == 270904126974590976 and message.channel.id == invocation_message.channel.id and ("you're not popular enough" in message.content or "Amazing job everybody, we racked up a total of" in message.content or "for an unsuccessful robbery" in message.content)

        try:
            return await self.bot.wait_for('message', check=check, timeout=300)

        except asyncio.TimeoutError:
            return None

    # Heist Listener
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id != 270904126974590976:
            return

        if not "is starting a bank robbery" in message.content:
            return
        
        await message.channel.set_permissions(message.guild.default_role, send_messages = None)
        await message.channel.edit(slowmode_delay = 6000)
        await message.channel.send("Good luck bank robbing this person! <a:rainbowheart:792504452900323329>")

        results = await self.get_heist_results(message)
        await message.channel.set_permissions(message.guild.default_role, send_messages = False)

        if results is None:
            await message.channel.send("Damn dank's probably dead right now you must have to wait a little bit")
        elif "you're not popular enough" in results.content or "for an unsuccessful robbery" in results.content:
            await message.channel.send("Well that sucks you didn't get enough people to join you heist, try again later I guess")
        else:
            await asyncio.sleep(3)
            if message.channel.id == 822567848400388106:
                await message.channel.send("Remember freeloaders get a 7 day ban so don't free load also to support us vote for us at https://top.gg/servers/784491141022220309/vote")

            msg = await message.channel.send(f"I hope that was a good heist!")
            await msg.add_reaction('✅')
            await msg.add_reaction('❌')
        
def setup(bot):
    bot.add_cog(HeistStarter(bot))