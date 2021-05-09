import discord
from discord.ext import commands

class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Add Whitelist
    @commands.command(aliases=['wl'])
    @commands.has_role(791516118120267806)
    async def whitelist(self, ctx, member: discord.Member=None):
        dbase = sqlite.connect('settings.db')
        cursor = dbase
        if member is None:
            await ctx.send('You need to mention a member!')

        else:
            cursor.execute("INSERT INTO user_id (user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET user_id = ?;", [member.id, member.id])

            await ctx.send(f'{member} is now whitelisted from being auto banned')

        dbase.close()
        dbase.commit()

def setup(client):
    client.add_cog(Settings(client))