import discord
from discord.ext import commands

import sqlite3

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    #On Member Join(Message)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        client = self.client

        await client.get_channel(784491141022220312).send(f'{member.mention}')
        join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
        join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for some info about how to get certain thing in the server and <#784547669619507201> for some self roles!')
        join_embed.add_field(name=f'__**User Info:**__', value=f'Date created: {member.created_at}\nUser ID: {member.id}', inline=False)
        await client.get_channel(784491141022220312).send(embed=join_embed)

    #On Member Join(Data Base)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        dbase = sqlite3.connect('bruni.db')
        cursor = dbase.cursor()
        user = f'{member.id}'
        guild = f'{ctx.guild.id}'
        cursor.execute(f"SELECT user_id FROM money_dono_logs WHERE user_id = '{member.id}'")
        result = cursor.fetchone()
        if result is None:
            amount = 0
            cursor.execute("INSERT INTO gaw_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO heist_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO money_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            cursor.execute("INSERT INTO special_event_dono_logs (guild_id, user_id, amount) VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = amount + ?;", [guild, user, amount, amount])
            print(f'Member added to database\nUSER: {member.name}\nID: {member.id}\n')
        else:
            pass
        dbase.commit()
        dbase.close()

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

def setup(client):
    client.add_cog(Events(client))