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
        client = self.client
        if time.time() - member.created_at.timestamp() < 2592000:

            channel = await member.create_dm()
            
            dm_embed = discord.Embed(title=f'You were banned from dank merchants', description=f'You were banned because your account was too young\nFill out [THIS](https://forms.gle/fZEuHNbpNH4LeJuPA) form to appeal and please state that you were banned because your account was too new', color=0x00ff00)
            await channel.send(embed=dm_embed)

            reason = 'Account to young in age'
            await member.ban(reason=reason)
            await client.get_channel(784491141022220312).send(f'{member.mention} was banned\nReason: Account age to young')

        else:
            join_embed = discord.Embed(title=f'Welcome To __**Dank Merchants**!__', description=f'**{member}** has joined the server!', color=0x00ff00)
            join_embed.add_field(name='What To Do', value=f'Make sure to go check out <#787343840108478474> for some info about how to get certain thing in the server and <#784547669619507201> for some self roles!')
            join_embed.add_field(name=f'__**User Info:**__', value=f'Date created: {member.created_at}\nUser ID: {member.id}', inline=False)
            await client.get_channel(784491141022220312).send(f'{member.mention}', embed=join_embed)

    #On Member Remove(Data Base)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user_id = member.id

        #Dono
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        cursor.execute("DELETE FROM donations WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM donations WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM donations WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM donations WHERE user_id = ?", [user_id])
        cursor.execute("DELETE FROM donations WHERE user_id = ?", [user_id])

        print(f'{user_id} removed from dono db\n')

        dbase.commit()
        dbase.close()

        #Economy
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        balance = 0

        cursor.execute("DELETE FROM economy WHERE user_id = ?", [user_id])

        dbase.commit()
        dbase.close()

    #Triggers
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(self.client.user.id) in message.content:
            embed = discord.Embed(title='Hello!', description='My prefix is `b!`\nUse the command `b!help` for help', color=0x00ff00)
            await message.channel.send(embed=embed)

        if str(765322777329664089) in message.content:
            user = message.author
            if not user.bot:
                await message.channel.send('If you are trying to donate to wiggle for a giveaway please ping someone else because he got blacklisted')
                await message.add_reaction(emoji='<a:blob:829822719372951592>')

            else:
                return

        if 'pls rob' in message.content:
            await message.channel.send('Ur dumb, rob is off')

        if 'pls steal' in message.content:
            await message.channel.send('Just why are you dumb')

    #Command Not Found
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'{ctx.author}: {error}')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{error} use the command `b!help` for a list of commands')

def setup(client):
    client.add_cog(Events(client))