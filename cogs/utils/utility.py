import discord
from discord.ext import commands

import asyncio
import sys
from datetime import datetime
import time
import psutil
import sys
import discord
import math

from config import *
from badges import *

class Utility(commands.Cog, name='utility', description='Some commands that will be helpful when needed'):
    def __init__(self, bot):
        self.bot = bot

    def natural_size(self, size_in_bytes: int):
        # turns the number of bytes into readable info
        units = ('B', 'KB', 'MB', 'GB', 'TB')

        power = int(math.log(size_in_bytes, 1024))

        return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"

    @commands.command(name='botinfo', description='Get some info on the bot')
    async def botinfo(self, ctx):
        info = ["```asciidoc" ,
                f"=== {self.bot.user} Info ===" ,
                f"• Latency                          :: {round(self.bot.latency * 1000, 2)}ms" ,
                f"• Discord.py Module Version        :: {discord.__version__}" ,
                f"• Python Version Info              :: {sys.version}"]

            # gets the current process
        proc = psutil.Process()

        # a context manager to speed up getting values we need
        with proc.oneshot():
            mem = proc.memory_full_info()
            info.append(f"• Physical memory                  :: {self.natural_size(mem.rss)}")
            info.append(f"• Virtual memory                   :: {self.natural_size(mem.vms)}")
            info.append(f"• Unique memory (to this process)  :: {self.natural_size(mem.uss)}")
                
            name = proc.name()
            pid = proc.pid
            thread_count = proc.num_threads()

            info.append(f"• Running on PID {pid} ({name}) with {thread_count} thread(s).")
            info.append("```")

        await ctx.send("\n".join(info))

    # Timer
    @commands.command(name='timer', description='Set a timer for up to 1000')
    async def count(self, ctx, number: int):
        try:
            if number < 0:
                await ctx.send('Must be a positve number')
            elif number > 1000:
                await ctx.send('Number must be under 1000')
            else:
                message = await ctx.send(number)
                while number != 0:
                    number -= 1
                    await message.edit(content=number)
                    await asyncio.sleep(1)
                await message.edit(content='Ended!')

        except ValueError:
            await ctx.send('Please provide a valid number')

    # Account Age
    @commands.command(name='date', description='Find out the date that your account was created')
    async def date(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        return await ctx.send(f'{member}\'s account was created on: <t:{int(member.created_at.timestamp())}:f>, <t:{int(member.created_at.timestamp())}:R>')

    # Ping
    @commands.command(name='ping', description='Shows the bots current ping', aliases=['ms'])
    async def ping(self, ctx: commands.Context):
        async with ctx.typing():
            start = time.perf_counter()
            message = await ctx.send("🏓 Ping...")
            end = time.perf_counter()
            duration = (end - start) * 1000

        await message.edit(content = f"🏓 Pong! Current latency: `{duration:.2f} ms`")

    # Server Info
    @commands.command(name='serverinfo', description='Shows the servers info', aliases=['si', 'server'])
    async def serverinfo(self, ctx):
        members = 0
        for member in ctx.guild.members:
            if not member.bot:
                members += 1
            else:
                pass

        total = (ctx.guild.member_count)

        info_embed = discord.Embed(title='Server Info/Stats', description='Here is the list of stats for the server', color=discord.Color.green())
        info_embed.set_thumbnail(url=ctx.guild.icon_url)
        info_embed.add_field(name='Server Name', value=ctx.guild.name)
        info_embed.add_field(name='Server Owner:', value=ctx.guild.owner)
        info_embed.add_field(name='Server ID', value=ctx.guild.id)
        info_embed.add_field(name='Server Human Count', value=members)
        info_embed.add_field(name='Total Member Count', value=total)
        await ctx.send(embed=info_embed)

    # Bug
    @commands.command()
    async def bug(self, ctx, *, bug):
        wiggle = self.bot.get_user(824010269071507536)
        embed = discord.Embed(title='Bug Report', description=f'**Reporter:** {ctx.author}({ctx.author.id})\n\n{bug}', color=discord.Color.red())
        embed.timestamp = datetime.utcnow()
        await wiggle.send(embed=embed)
        await ctx.send('Bug sent!')
    
    # Suggest
    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        embed = discord.Embed(title=f'Suggestion From {ctx.author}', description=f'**Suggestion:**\n{suggestion}')
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f'User id: {ctx.author.id}')
        msg = await self.bot.get_channel(827293945003376650).send(embed=embed)
        await msg.add_reaction('✔')
        await msg.add_reaction('✖')
        await ctx.send('Suggestion sent in <#827293945003376650>')

    """PROFILE STUFF BELOW"""

    def get_donation(self, user):
        dbase = sqlite3.connect('dono.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT total, money FROM donations WHERE user_id == '{user.id}'")
        result = cursor.fetchone()
        if result is None:
            result = [0, 0]
            return result

        else:
            dbase.close()
            return result

    def detail(self, ctx, user):
        details = 'Member, '
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

    def badges_(self, ctx, user):
        badges = ''
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

    




    # Profile
    @commands.command(name='profile', description='Check your server profile', aliases=['me', 'user', 'ui'])
    async def profile(self, ctx, member: discord.Member=None):
        user = member or ctx.author
        
        amount = self.get_donation(user)
        badges_ = self.badges_(ctx, user)
        bumps = self.bumps(user)
        details = self.detail(ctx, user)

        embed = discord.Embed(title=f"{user}'s Server Profile", description=badges_, color=user.color)
        embed.add_field(name='Dank Memer Donations:', value=f'`⏣{"{:,}".format(amount[0])}`')
        embed.add_field(name='Real Money Donations:', value=f'`${amount[1]} USD`')
        embed.add_field(name='Server Bump Stats:', value=f'`{bumps}` successful bumps')
        embed.add_field(name='Member Details', value=details[:-2], inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=user.id, icon_url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))