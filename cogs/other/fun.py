import discord
from discord.ext import commands

import aiohttp
from typing import List

from config import *

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Fun(commands.Cog, name='fun', description='Some fun commands'):
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

    '''
    Tic Tac Toe
    '''
    


    # TTT
    @commands.command(name='tictactoe', decription='Play tic tac toe with a friend(still has some bugs)', aliases=['ttt'])
    async def ttt(self, ctx: commands.Context):
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

def setup(bot):
    bot.add_cog(Fun(bot))