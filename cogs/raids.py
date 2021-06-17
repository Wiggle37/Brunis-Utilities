from discord.ext import commands
import discord
import asyncio
 
class massEvents(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.raiders = {}
    
    @commands.group(invoke_without_command = True)
    async def raid(self, ctx):
        raid_help_embed = discord.Embed(
            title = "How to boss raids 101",
            description = "Boss raids commands",
            colour = 0x4db59a
        )
 
        raid_help_embed.add_field(name = "How to start a raid?", value = "```b!raid start```", inline = True)
        raid_help_embed.add_field(name = "How to join a raid?", value = "```join raid```", inline = True)
 
        raid_help_embed.add_field(
            name = "What even are boss raids?",
            value = "A creature spawned out of nowhere and threatened the stability of the server!\nWe need people to team up against this creature and restore peace and tranquility and defeating this creature",
            inline = False
        )
 
        await ctx.send(embed = raid_help_embed)
 
    async def read_messages(self, ctx):
        def check(message):
            return message.content.lower() == 'join raid' and message.channel == ctx.channel
        
        while True:
            try:
                valid_message = await self.bot.wait_for("message", check = check, timeout = 30)
                if self.raiders.get(valid_message.author.id) is None:
                    await valid_message.add_reaction(":pog:790995076339859547:")
                    self.raiders[valid_message.author.id] = valid_message.author.name
                else:
                    await valid_message.reply("You already joined the raid!")
 
            except asyncio.TimeoutError:
                pass
 
    @raid.command()
    async def start(self, ctx):
        raid_start_embed = discord.Embed(title = "A boss is here!", colour = 0x4c1a33)
        raid_start_embed.add_field(name = "It's Tiny Tortle", value = "Quick, type ```join raid``` to fight the boss!")
 
        await ctx.send(embed = raid_start_embed)
 
        try:
            await asyncio.wait_for(self.read_messages(ctx), 60)
        except asyncio.TimeoutError:
            pass # this will be triggered
 
        results = []
 
        if len(self.raiders) == 0:
            return await ctx.send("Wow no one participated?")
        await ctx.send("Good job people, we managed to defeat the boss!")
 
        for name in self.raiders.values():
            # add currency here
            results.append(f"{name} got away with too many coins")
        
 
        prefix = "```\n"
        suffix = "\n```"
        sending_res = prefix
        # avoiding hitting the 2000 char limit for messages
        for res in results:
            if len(sending_res) + len(res) > 1995:
                sending_res += suffix
                await ctx.send(sending_res)
                sending_res = prefix
 
            else:
                sending_res += res + "\n"
        
        sending_res += suffix
        await ctx.send(sending_res)

def setup(client):
    client.add_cog(massEvents(client))