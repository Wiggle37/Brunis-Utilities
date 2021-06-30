from datetime import datetime
import discord
from discord.ext import commands
import sqlite3

class Lottery(commands.Cog, name='lottery', description='Lottery commands for hosting lottery events'):

    def __init__(self, client):
        self.client = client

    def get_table(self):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        tables = cursor.fetchall()
        dbase.close()
        return tables[0][0]

    #Start Lottery
    @commands.command(name='startlottery')
    async def startlottery(self, ctx, name):
        def check(message):
            return ctx.author == message.author and ctx.channel == message.channel
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        await ctx.reply('Please send "yes" to reset all data from the before lottery and make a new one.')
        confirm = await self.client.wait_for('message', check=check, timeout=30)
        if confirm.clean_content == 'yes':
            lotto = self.get_table()
            cursor.execute(f"DROP TABLE '{lotto}'")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{name}" (
	                "user_id"	INTEGER UNIQUE,
	                "tickets"	INTEGER DEFAULT 0
        );""")

        await ctx.send(f'All former lottery data reset and made new lottery with the name **{name}**')

        dbase.commit()
        dbase.close()

    #End Lottery
    @commands.command(name='endlottery')
    async def endlottery(self, ctx):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        dbase.commit()
        dbase.close()

    #Add Tickets
    @commands.command(name='addticket')
    async def addticket(self, ctx, member: discord.Member, amount: int=1):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        lotto = self.get_table()

        cursor.execute(f"INSERT INTO '{lotto}' (user_id, tickets) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET tickets = tickets + ?;", [member.id, amount, amount])
        embed = discord.Embed(title='Tickets Updated', description=f'**Member:** {member.name}\n**Tickets:** {amount}', color=0x2e5090)
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    #Remove Tickets
    @commands.command(name='removeticket')
    async def removeticket(self, ctx, member: discord.Member, amount: int=1):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        lotto = self.get_table()

        cursor.execute(f"INSERT INTO '{lotto}' (user_id, tickets) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET tickets = tickets - ?;", [member.id, amount, amount])
        embed = discord.Embed(title='Tickets Updated', description=f'**Member:** {member.name}\n**Tickets:** {amount}', color=0x2e5090)
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    #View Tickets
    @commands.command()
    async def tickets(self, ctx, member: discord.Member=None):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()
        member = member or ctx.author

        lotto = self.get_table()

        cursor.execute(f"SELECT tickets FROM '{lotto}' WHERE user_id = '{member.id}'")
        tickets = cursor.fetchone()
        if tickets is None:
            return await ctx.send('You are not entered in the current lottery')
        
        embed = discord.Embed(title=f'Lottery Details For {member.name}', description=f'**Tickets:** {tickets[0]}', color=0x2e5090)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

    #View All Tickets
    @commands.command()
    async def viewlotto(self, ctx):
        dbase = sqlite3.connect('lotto.db')
        cursor = dbase.cursor()

        lotto = self.get_table()
        
        cursor.execute(f"SELECT user_id, tickets FROM '{lotto}'")
        results = cursor.fetchall()
        if results is None:
            return await ctx.send('There is nobody in the current lottery')

        msg = ''
        num = 0

        for i in results:
            user = self.client.get_user(i[0])
            msg += f'**{user.name}**: {i[1]}\n'
            num += 1

        embed = discord.Embed(title='Lottery Tickets List', description=msg, color=0x2e5090)
        await ctx.send(embed=embed)

        dbase.commit()
        dbase.close()

def setup(client):
    client.add_cog(Lottery(client))