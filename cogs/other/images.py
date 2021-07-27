import discord
from discord.ext import commands

import aiohttp

from config import *

class Images(commands.Cog, name='images', description='Some image commands'):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    # Dog
    @commands.command(name='dog', description='Get a random picture of a dog', aliases=['doggo', 'bark', 'bork'])
    async def dog(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/dog') as response:
            json = await response.json()
        embed = discord.Embed(title="Doggo 🐕‍🦺", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Cat
    @commands.command(name='cat', description='Get a random picture of a cat *meow*', aliases=['kitty', 'meow', 'pussy'])
    async def cat(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/cat') as response:
            json = await response.json()
        embed = discord.Embed(title="Kitty Cat 🐈", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Cat GIF
    @commands.command(name='catgif', description='Get a GIF of a cat')
    async def catgif(self, ctx):
        embed = discord.Embed(title='Cat Gif 🐈')
        embed.set_image(url='https://cataas.com/cat/gif')
        await ctx.send(embed=embed)

    # HTTP Cat
    @commands.command(name='HTTPcat', description='Get the cat related to the HTTP error code')
    async def httpcat(self, ctx, error: int=None):
        error_codes = [100, 101, 102, 200, 201, 202, 203, 204, 206, 207, 300, 301, 302, 303, 304, 305, 306, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 429, 431, 444, 450, 451, 499, 500, 501, 502, 503, 504, 506, 107, 508, 509, 510, 511, 599]
        if error is None or error not in error_codes:
            error = 404

        embed = discord.Embed(title="Error Cat 🐈", color=discord.Color.purple())
        embed.set_image(url=f'https://http.cat/{error}')
        await ctx.send(embed=embed)

    # Panda
    @commands.command(name='panda', description='Get a random picture of a panda')
    async def panda(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/panda') as response:
            json = await response.json()
        embed = discord.Embed(title="Panda 🐼", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Red Panda
    @commands.command(name='redpanda', description='Get a random picture of a red panda')
    async def redpanda(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/red_panda') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Red Panda 🐼", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    # Bird
    @commands.command(name='bird', description='Get a random picture of a bird')
    async def bird(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/birb') as response:
            json = await response.json()
        embed = discord.Embed(title="Bird 🐥", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Fox
    @commands.command(name='fox', description='Get a random picture of a fox')
    async def fox(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/fox') as response:
            json = await response.json()
        embed = discord.Embed(title="Fox 🦊", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Koala
    @commands.command(name='koala', description='Get a random picture of a koala')
    async def koala(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/koala') as response:
            json = await response.json()
        embed = discord.Embed(title="Koala 🐨", color=discord.Color.purple())
        embed.set_image(url=json['link'])
        await ctx.send(embed=embed)

    # Axolotl
    @commands.command(name='axolotl', description='Get a picture of an axolotl')
    async def axolotl(self, ctx):
        async with self.session.get('https://axoltlapi.herokuapp.com/') as response:
            json = await response.json()
        embed = discord.Embed(title="Axolotl", color=discord.Color.purple())
        embed.set_image(url=json['url'])
        embed.set_footer(text=f"Fun Fact About Axolotls: {json['facts']}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))