import discord
from discord.ext import commands

import sqlite3

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    '''
    MEMBER EVENTS
    '''
    #On Member Join(Message(Add Data Base))
    @commands.Cog.listener()
    async def on_member_join(self, member):
        client = self.client

        join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
        join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for some info about how to get certain thing in the server and <#784547669619507201> for some self roles!')
        join_embed.add_field(name=f'__**User Info:**__', value=f'Date created: {member.created_at}\nUser ID: {member.id}', inline=False)
        await client.get_channel(784491141022220312).send(f'{member.mention}', embed=join_embed)

    #On Member Remove(Data Base)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()

        user_id = member.id

        cursor.execute("DELETE FROM gaw_dono_logs WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM heist_dono_logs WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM event_dono_logs WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM special_event_dono_logs WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM money_dono_logs WHERE user_id = ?", [user_id])

        print(f'{user_id} removed from db\n')

        dbase.commit()
        dbase.close()

    '''
    TRIGGERS
    '''
    #Rob
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('pls rob'):
            await message.channel.send('You stole NOTHING LMFAO\nRob is turned off dumbass')

def setup(client):
    client.add_cog(Events(client))