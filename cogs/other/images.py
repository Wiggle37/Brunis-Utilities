import discord
from discord.ext import commands

import aiohttp

from config import *

class Images(commands.Cog, name='images', description='Get some pictures of some animals'):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    # Dog
    @commands.command(name='dog', description='Get a random picture of a dog', aliases=['doggo', 'bark', 'bork'])
    async def dog(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/dog') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Doggo 🐕‍🦺", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    # Cat
    @commands.command(name='Cat', description='Get a random picture of a cat *meow*', aliases=['kitty', 'meow', 'pussy'])
    async def cat(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/cat') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Kitty Cat 🐈!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    # Panda
    @commands.command(name='panda', description='Get a random picture of a panda')
    async def panda(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/panda') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Panda 🐼", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
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
            dogjson = await response.json()
        embed = discord.Embed(title="Bird 🐥", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    # Fox
    @commands.command(name='fox', description='Get a random picture of a fox')
    async def fox(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/fox') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Fox 🦊", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    # Koala
    @commands.command(name='koala', description='Get a random picture of a koala')
    async def koala(self, ctx):
        async with self.session.get('https://some-random-api.ml/img/koala') as response:
            dogjson = await response.json()
        embed = discord.Embed(title="Koala 🐨", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Images(bot))