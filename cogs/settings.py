import discord
from discord.ext import commands

import sqlite3

class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Add Whitelist
    @commands.command(aliases=['wl'])
    @commands.has_role(791516118120267806)
    async def whitelist(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('settings.db')
        cursor = dbase.cursor()

        user = member.id

        if member is None:
            await ctx.send('You need to mention a member!')

        else:
            cursor.execute(f"SELECT user_id FROM whitelists WHERE user_id = '{member.id}'")
            wl = cursor.fetchone()
            if wl is None:
                cursor.execute("INSERT INTO whitelists (user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET user_id = ?;", [user])

                await ctx.send(f'{member} is now whitelisted from being auto banned')

            else:
                await ctx.send('That user is already whitelisted')

        dbase.commit()
        dbase.close()
        

def setup(client):
    client.add_cog(Settings(client))