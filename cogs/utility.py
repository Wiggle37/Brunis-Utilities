import discord
from discord.ext import commands
import asyncio

class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Timer
    @commands.command()
    async def count(self, ctx, number: int):
        client = self.client
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

def setup(client):
    client.add_cog(Utility(client))