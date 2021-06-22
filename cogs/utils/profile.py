from badges import *
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

class Profile(commands.Cog, name='Profile', description='See your server profile'):

    def __init__(self, client):
        self.client = client

    def get_donation(self, user):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT total, money FROM donations WHERE user_id == '{user.id}'")
        result = cursor.fetchone()
        if result is None:
            result = [0, 0]
            return result

        else:
            return result

        dbase.close()

    def detail(self, ctx, user):
        details = ''
        member = discord.utils.find(lambda r: r.id == 784529268881227796, ctx.message.guild.roles)
        if member in user.roles:
            details += 'Member, '
        staff = discord.utils.find(lambda r: r.id == 791516118120267806, ctx.message.guild.roles)
        if staff in user.roles:
            details += 'Staff, '
        gaw = discord.utils.find(lambda r: r.id == 785198646731604008, ctx.message.guild.roles)
        if gaw in user.roles:
            details += 'Giveaway Manager, '
        heist = discord.utils.find(lambda r: r.id == 785631914010214410, ctx.message.guild.roles)
        if heist in user.roles:
            details += 'Heist Manager, '
        event = discord.utils.find(lambda r: r.id == 791516116710064159, ctx.message.guild.roles)
        if event in user.roles:
            details += 'Event Manager, '
        auction = discord.utils.find(lambda r: r.id == 802645887063031818, ctx.message.guild.roles)
        if auction in user.roles:
            details += 'Auctioneer, '

        return details

    def bumps(self, user):
        dbase = sqlite3.connect('bump.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT bump FROM bumps WHERE user_id == '{user.id}'")
        result = cursor.fetchone()
        if result is None:
            return 0

        else:
            return result[0]

    def badges(self, ctx, user):
        badges = '‏‏‎ ‎'
        staff_ = discord.utils.find(lambda r: r.id == 791516118120267806, ctx.message.guild.roles)
        if staff_ in user.roles:
            badges += f'{staff.emoji} '

        topdonor_ = discord.utils.find(lambda r: r.id == 793189820151234620, ctx.message.guild.roles)
        if topdonor_ in user.roles:
            badges += f'{topdonor.emoji} '

        # Donations
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()
        cursor.execute(f"SELECT total FROM donations WHERE user_id = '{user.id}'")
        total = cursor.fetchone()[0]
        donor_emojis = {
            5000000: mil5.emoji,      # 5 million
            10000000: mil10.emoji,    # 10 million
            25000000: mil25.emoji,    # 25 million
            50000000: mil50.emoji,    # 50 million
            100000000: mil100.emoji,  # 100 million
            250000000: mil250.emoji,  # 250 million
            500000000: mil500.emoji,  # 500 million
            1000000000: bil1.emoji,   # 1 billion
            2500000000: bil2_5.emoji, # 2.5 billion
            5000000000: bil5.emoji    # 5 billion
        }
        for amount, emoji in donor_emojis.items():
            if total < amount:
                break
            badges += f'{emoji} '
        dbase.close()

        # Levels
        level_emojis = {
            level5.role_id: level5.emoji,     # Level 5
            level10.role_id: level10.emoji,   # Level 10
            level15.role_id: level15.emoji,   # Level 15
            level20.role_id: level20.emoji,   # Level 20
            level30.role_id: level30.emoji,   # Level 30
            level40.role_id: level40.emoji,   # Level 40
            level50.role_id: level50.emoji,   # Level 50
            level69.role_id: level69.emoji,   # Level 69
            level100.role_id: level100.emoji, # Level 100
        }
        for role_id, emoji in level_emojis.items():
            role = discord.utils.find(lambda r: r.id == role_id, ctx.message.guild.roles)
            if role in user.roles:
                badges += f'{emoji} '

        return badges

    @commands.command(name='profile', description='Check your server profile', aliases=['me', 'user'])
    async def profile(self, ctx, member: discord.Member=None):
        user = member or ctx.author
        
        amount = self.get_donation(user)
        badges = self.badges(ctx, user)
        bumps = self.bumps(user)
        details = self.detail(ctx, user)

        embed = discord.Embed(title=f"{user}'s Server Profile", description=badges[:-1], color=user.color)
        embed.add_field(name='Dank Memer Donations:', value=f'`⏣{"{:,}".format(amount[0])}`')
        embed.add_field(name='Real Money Donations:', value=f'`${amount[1]} USD`')
        embed.add_field(name='Server Bump Stats:', value=f'`{bumps}` successful bumps')
        embed.add_field(name='Member Details', value=details[:-2], inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=user.id, icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(name='badges', description='Check all the badges for the `b!profile` command')
    async def badges(self, ctx):
        level_emojis = [level5, level10, level15, level20, level30, level40, level50, level69, level100]
        levels_ = ''
        for emoji in level_emojis:
            levels_ += f'{emoji.name} - {emoji.emoji}\n'
        
        dono_emojis = [mil5, mil10, mil25, mil50, mil100, mil250, mil500, bil1, bil2_5, bil5, topdonor]
        donations_ = ''
        for dono in dono_emojis:
            donations_ += f'{dono.name} - {dono.emoji}\n'

        embed = discord.Embed(title='All The Badges', description='A list of all the profile badges')
        embed.add_field(name='Levels', value=levels_, inline=False)
        embed.add_field(name='Donations', value=donations_)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Profile(client))