import discord
from discord.ext import commands

class NotValidInteger(commands.CommandError):
    pass

class ValidInteger(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            float(argument.replace("m","e6").replace("k","e3"))
            ret = float(eval(argument.replace("k","e3").replace("m", "e6")))
            if not ret.is_integer():
                raise NotValidInteger
            return int(ret)
                
        except ValueError:
            raise NotValidInteger