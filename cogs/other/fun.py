from discord.ext import commands
import http

class Fun(commands.Cog, name='fun', description='Some fun commands'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='urban', description='Find the definition to what you are searching for on the urban dictionary')
    async def urban(self, ctx, *, search: commands.clean_content):
        async with ctx.channel.typing():
            try:
                url = await http.get(f"https://api.urbandictionary.com/v0/define?term={search}", res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url["list"]):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")

def setup(client):
    client.add_cog(Fun(client))