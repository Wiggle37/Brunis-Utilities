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
        if member.guild.id == 784491141022220309:
            if time.time() - member.created_at.timestamp() < 1814400:
                channel = await member.create_dm()
                    
                dm_embed = discord.Embed(title=f'You were banned from dank merchants', description=f'You were banned because your account was too young\nFill out [THIS](https://forms.gle/fZEuHNbpNH4LeJuPA) form to appeal and please state that you were banned because your account was too new', color=0x00ff00)
                await channel.send(embed=dm_embed)

                reason = 'Account to young in age'
                await member.kick(reason=reason)
                await self.client.get_channel(784491141022220312).send(f'{member.mention} was banned\nReason: Account age to young')

            else:
                join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
                join_embed.set_thumbnail(url=member.avatar_url)
                join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for the rules in the server and all the perks\nAnd go get some roles in <#784547669619507201> to get notified when certain things happen\n\nAnd if you have any questions go wait for someone in <#787761394664996865> and they will be there as soon as possible!')
                join_embed.add_field(name=f'__**User Info:**__', value=f'Date created: {member.created_at}\nUser ID: {member.id}', inline=False)
                await self.client.get_channel(784491141022220312).send(f'{member.mention}', embed=join_embed)
        
        else:
            pass
        
    #Triggers
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if str(self.client.user.id) in message.content:
            embed = discord.Embed(title='Hello!', description='My prefix is `b!`\nUse the command `b!help` for help', color=0x00ff00)
            await message.channel.send(embed=embed)

        if 'wiggle' in message.content:
            if not user.bot:
                await message.channel.send('why you be saying my name, huh?')
                await message.add_reaction(emoji='<a:blob:829822719372951592>')

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