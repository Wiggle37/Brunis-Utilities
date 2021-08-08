import discord
from discord.ext import commands

import aiosqlite
import time

from config import *

class Events(commands.Cog, name='Events', command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    '''
    MEMBER EVENTS
    '''
    # On Member Join(Message)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 784491141022220309:
            if time.time() - member.created_at.timestamp() < 1814400:      
                try:              
                    dm_embed = discord.Embed(title=f'You were banned from dank merchants', description=f'You were banned because your account was too young\nYou will be unbanned when your account is over the age of 3 weeks old(21 days)\nIn the mean time you can join [this](https://discord.gg/ubtz7gK2js) server if you have anymore questions', color=0x00ff00)
                    await member.send(embed=dm_embed)
                except:
                    pass

                reason = 'Account to young in age'
                await member.kick(reason=reason)
                embed = discord.Embed(title=f'{member.name} Was Kicked', description=f'They were kicked because thier account age was too young.\nAccount Creation Date: <t:{int(member.created_at.timestamp())}:f>\nThey need <t:{int(member.created_at.timestamp())}:R>')
                await self.bot.get_channel(805620755446366280).send(f'**{member}** was banned because their account age was not at least 3 weeks old. They will be unbanned when their account is old enough. Their account was made <t:{int(member.created_at.timestamp())}:f>, <t:{int(member.created_at.timestamp())}:R>')

            else:
                await self.bot.get_channel(870276752440692776).send(member.mention, delete_after=7)

                try:
                    dm_embed = discord.Embed(title=f'Welcome To Dank Merchants!', description=f'In case of you getting banned from the server join [this](https://discord.gg/ubtz7gK2js) server to appeal, **DO NOT OPEN A TICKET UNLESS YOU ARE BANNED OPENING A TICKET FOR NO REASON WASTES MODS TIME**', color=0x00ff00)
                    await member.send(embed=dm_embed)
                except:
                    pass

                members_count = 0
                for i in member.guild.members:
                    if not i.bot:
                        members_count += 1
                    else:
                        pass

                if CONFIG["settings"]["heists"]["heistmode"]:
                    await self.bot.get_channel(870193314413019216).send(f'{member.mention} has joined the server around a heist time, when the heist starts you may join! <#870284332810526750>')

                elif not CONFIG["settings"]["heists"]["heistmode"]:
                    join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member.mention}** has joined the server!', color=0x00ff00)
                    join_embed.set_thumbnail(url=member.avatar.url)
                    join_embed.add_field(name='__**What To Do:**__', value=f'<#787343840108478474> ➞ Read the rules of Dank Merchants\n<#784547669619507201> ➞ Get some self roles\n<#863437182131503134> ➞ Check out our amazing grinder perks\n\nAnd any other questions may be asked in <#787761394664996865>')
                    join_embed.add_field(name=f'__**More Info:**__', value=f'Account Creation: <t:{int(member.created_at.timestamp())}:f>\nUser ID: {member.id}\nMember Count: {members_count} humans', inline=False)
                    await self.bot.get_channel(870193314413019216).send(embed=join_embed)
        
        else:
            return

    # Text Response
    @commands.Cog.listener("on_message")
    async def text_response(self, message):
        async with aiosqlite.connect('autoresponse.db') as dbase:
            cursor = await dbase.execute("SELECT trigger, response FROM text")
            text_response = await cursor.fetchall()

        if text_response is None:
            return

        cleaned_content = message.content.lower()

        for trigger, response in text_response:
            if trigger in cleaned_content and not message.author.bot:
                try:
                    await message.channel.send(response)
                except:
                    pass
        
    # Emoji Reaction
    @commands.Cog.listener("on_message")
    async def emoji_react(self, message):
        async with aiosqlite.connect('autoresponse.db') as dbase:
            cursor = await dbase.execute("SELECT trigger, emoji FROM emoji")
            emoji_react = await cursor.fetchall()

        if emoji_react is None:
            return

        cleaned_content = message.content.lower()

        for trigger, emoji in emoji_react:
            if trigger in cleaned_content and not message.author.bot:
                try:
                    await message.add_reaction(emoji)
                except:
                    pass
    
    #Triggers
    @commands.Cog.listener()
    async def on_message(self, message):
        if str('heist') in message.content and message.guild.id == 784491141022220309:
            if CONFIG["settings"]["heists"]["heistmode"] and not message.channel.id == 822567848400388106 and not message.author.id == self.bot.user.id:
                await message.channel.send('<#870284332810526750>')

def setup(bot):
    bot.add_cog(Events(bot))