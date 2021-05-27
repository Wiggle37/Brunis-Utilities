import discord
from discord.ext import commands
import sqlite3
import time

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
    MEMBER EVENTS
    '''
    #On Member Join(Message(Add Data Base))
    @commands.Cog.listener()
    async def on_member_join(self, member):
        seconds = time.time() - member.created_at.timestamp()
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60

        days = seconds // seconds_in_day
        hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
        minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute

        if member.guild.id == 784491141022220309:
            if time.time() - member.created_at.timestamp() < 1814400:
                channel = await member.create_dm()
                    
                dm_embed = discord.Embed(title=f'You were banned from dank merchants', description=f'You were banned because your account was too young\nYou will be unbanned when your account is over the age of 3 weeks old(21 days)\nIn the mean time you can join (this)[https://discord.gg/ubtz7gK2js] server if you have anymore questions', color=0x00ff00)
                await channel.send(embed=dm_embed)

                reason = 'Account to young in age'
                await member.kick(reason=reason)
                await self.client.get_channel(784491141022220312).send(f'**{member}** was banned because their account age was not at least 3 weeks old. They will be unbanned when their account is old enough. <@!{member.id}>s account was made {int(days)} days {int(hours)} hours {int(minutes)} minutes ago')

            else:
                channel = await member.create_dm()
                    
                dm_embed = discord.Embed(title=f'Welcome To Dank Merchants!', description=f'In case of you getting banned from the server join [this](https://discord.gg/ubtz7gK2js) server to appeal', color=0x00ff00)
                await channel.send(embed=dm_embed)
                join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
                join_embed.set_thumbnail(url=member.avatar_url)
                join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for the rules in the server and all the perks\nAnd go get some roles in <#784547669619507201> to get notified when certain things happen\n\nAnd if you have any questions go wait for someone in <#787761394664996865> and ask your question and they will be there as soon as possible!')
                join_embed.add_field(name=f'__**User Info:**__', value=f'Time Created: {int(days)} days {int(hours)} hours {int(minutes)} minutes ago\nUser ID: {member.id}', inline=False)
                await self.client.get_channel(784491141022220312).send(f'{member.mention}', embed=join_embed)
        
        else:
            return
    
    
    #Triggers
    @commands.Cog.listener()
    async def on_message(self, message):
        triggers = {
        '<>': '<a:letterW:847207145535569990> <a:letterI:847206935992467476> <a:letterG:847206884700061707> <a:letterG:847206884700061707> <a:CS_AlphabetL:847206998138159156> <a:CS_AlphabetE:847206847476006972> <a:hehehe:>'
    }
        user = message.author
        if str(self.client.user.id) in message.content:
            embed = discord.Embed(title='Hello!', description='My prefix is `b!`\nUse the command `b!help` for help', color=0x00ff00)
            await message.channel.send(embed=embed)

        for trigger, response in triggers.items():
            if trigger in message.clean_content.lower():
                if not user.bot:
                    await message.channel.send(response)

                else:
                    return

        if 'pls rob' in message.content:
            await message.channel.send('Ur dumb, rob is off')

        if 'pls steal' in message.content:
            await message.channel.send('Just why are you dumb')

        if 'dyno' in message.content:
            await message.channel.send('gae')

    

def setup(client):
    client.add_cog(Events(client))