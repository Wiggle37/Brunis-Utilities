import discord
from discord.ext import commands
import asyncio

class HeistStarter(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_heist_results(self, invocation_message):
        def check(message):
            return message.author.id == 270904126974590976 and message.channel.id == invocation_message.channel.id and ("you're not popular enough" in message.content or "Amazing job everybody, we racked up a total of" in message.content or "for an unsuccessful robbery" in message.content)

        try:
            return await self.client.wait_for('message', check=check, timeout=300)

        except asyncio.TimeoutError:
            return None

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id != 270904126974590976:
            return

        if not "is starting a bank robbery" in message.content:
            return
        
        await message.channel.set_permissions(message.guild.default_role, send_messages = True)
        await message.channel.edit(slowmode_delay = 300)
        await message.channel.send("Good luck!<a:rainbowheart:792504452900323329>")

        results = await self.get_heist_results(message)
        await message.channel.set_permissions(message.guild.default_role, send_messages = False)

        if results is None:
            await message.channel.send("Damn dank's probably dead")
        elif "you're not popular enough" in results.content or "for an unsuccessful robbery" in results.content:
            await message.channel.send("Well that sucks")
        else: 
            await message.channel.send("I hope that was a good heist!")
 
        
def setup(client):
    client.add_cog(HeistStarter(client))