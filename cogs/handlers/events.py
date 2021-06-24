import discord
from discord.ext import commands
import sqlite3
import time
from datetime import datetime

class Events(commands.Cog, name='Events', command_attrs=dict(hidden=True)):

    def __init__(self, client):
        self.client = client
        self.self_roles_channel = self.client.get_channel(784547669619507201)

    '''
    MEMBER EVENTS
    '''
    #On Member Join(Message(Add Data Base))
    @commands.Cog.listener()
    async def on_member_join(self, member):
        seconds = time.time() - member.created_at.timestamp()
        seconds_in_day = 60 * 60 * 24
        days = seconds // seconds_in_day

        if member.guild.id == 784491141022220309:
            if time.time() - member.created_at.timestamp() < 1814400:
                channel = await member.create_dm()
                    
                dm_embed = discord.Embed(title=f'You were banned from dank merchants', description=f'You were banned because your account was too young\nYou will be unbanned when your account is over the age of 3 weeks old(21 days)\nIn the mean time you can join [this](https://discord.gg/ubtz7gK2js) server if you have anymore questions', color=0x00ff00)
                await channel.send(embed=dm_embed)

                reason = 'Account to young in age'
                await member.kick(reason=reason)
                await self.client.get_channel(784491141022220312).send(f'**{member}** was banned because their account age was not at least 3 weeks old. They will be unbanned when their account is old enough. Their account was made {int(days)} days ago')

            else:
                ping_message = await self.self_roles_channel.send(member.mention)
                await ping_message.delete(delay = 7)

                try:
                    dm_embed = discord.Embed(title=f'Welcome To Dank Merchants!', description=f'In case of you getting banned from the server join [this](https://discord.gg/ubtz7gK2js) server to appeal', color=0x00ff00)
                    await member.send(embed=dm_embed)
                except:
                    pass

                members = 0
                for member in member.guild.members:
                    if member.bot:
                        pass
                    else:
                        members += 1

                join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
                join_embed.set_thumbnail(url=member.avatar_url)
                join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for the rules in the server and all the perks\n\nAnd if you have any questions go wait for someone in <#787761394664996865> and ask your question and staff will be there as soon as possible! Also in case of you getting banned join the ban appeal server [here](https://discord.gg/f8steRTWQj)')
                join_embed.add_field(name=f'__**More Info:**__', value=f'Time Created: {int(days)} days ago\nUser ID: {member.id}\nWe are now at {members} members', inline=False)
                await self.client.get_channel(784491141022220312).send(embed=join_embed)

                if members == 5000:
                    await self.client.get_channel(784491141022220312).send('We are now at 5,000 members!!! 🎉🎉🎉 The events and giveaways will begin soon!')
        
        else:
            return

    @commands.Cog.listener("on_message")
    async def text_response(self, message):
        dbase = sqlite3.connect('autoresponse.db')
        cur = dbase.cursor()

        cur.execute("SELECT trigger, response FROM text")
        text_response = cur.fetchall()
        dbase.close()

        if text_response is None:
            return

        cleaned_content = message.content.lower()

        for trigger, response in text_response:
            if trigger in cleaned_content and not message.author.bot:
                await message.channel.send(response)
        
    @commands.Cog.listener("on_message")
    async def emoji_react(self, message):
        dbase = sqlite3.connect('autoresponse.db')
        cur = dbase.cursor()

        cur.execute("SELECT trigger, emoji FROM emoji")
        emoji_react = cur.fetchall()
        dbase.close()

        if emoji_react is None:
            return

        cleaned_content = message.content.lower()

        for trigger, emoji in emoji_react:
            if trigger in cleaned_content and not message.author.bot:
                await message.add_reaction(emoji)
    
    
    #Triggers
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if str(self.client.user.id) in message.content:
            embed = discord.Embed(title='Hello!', description='My prefix is `b!`\nUse the command `b!help` for help', color=0x00ff00)
            await message.channel.send(embed=embed)

    #Other Server Prevention
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = [
            784491141022220309, # Merchants
            831346501702647888, # Merchants Ban Appeal
            824723149891174411, # Ban Royale
            810233137988239430, # Brunis Support
            844759955815006219, # Brunis Emojis
        ]

        if guild.id in guilds:
            return
        
        else:
            await guild.leave()
            print('Someone got the invite link again somehow *smh*')

def setup(client):
    client.add_cog(Events(client))