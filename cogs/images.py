import discord
from discord.ext import commands

import aiohttp
from aiohttp import ClientSession

import requests

class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Dog
    @commands.command()
    async def dog(dog, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            dogjson = await request.json()

        embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
        embed.set_image(url=dogjson['link'])
        await ctx.send(embed=embed)

    #Cat
    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://aws.random.cat/meow')
        data = response.json()

        embed = discord.Embed(title='Kitty Cat 🐈', color=discord.Colour.purple())
        embed.set_image(url=data['file'])            
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Images(client))