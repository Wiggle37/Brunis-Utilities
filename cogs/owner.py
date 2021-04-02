import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Announce
    @commands.command()
    async def announce(self, ctx, *, msg):
        client = self.client

        await client.get_channel(827293945003376650).send(msg)
        await client.get_channel(827293945003376650).send(f'\nMSG sent by: **{ctx.message.author}**')
        await ctx.send('Announcement sent to <#827293945003376650>')

    #Update
    @commands.command()
    async def update1(self, ctx):
        client = self.client
        await ctx.message.delete()
        await client.get_channel(827293945003376650).send(f'Ok, I am very proud to announce the newest bot in our server! **{client.user}**!\nSo for this bot is still so much in developement that it may have a some errors(probally a lot...)so if you ever see one PLEASE send a DM to <@765322777329664089> explaining the issue as much as you can so I can so my best to fix it. And also FYI me(<@765322777329664089>) and bruni(<@784172569153503332>) have full access to all of these command to bypass\n\nSoon I would like to add a vouching system which is the same as the other vouch bot but I make it(this will not bec coming this month because I other things to work on with this bot that are more important)! So now let talk commands who can access what commands and what they do\n\n__**Command Access:**__\n- `b!dono <member / id>` -> anyone can you this command \nAt the moment the only way to check your own donation is by doing `b!dono <@your user / id>` I know this is kind of incovenient but it is what it is and will try to be fixed soon')

    @commands.command()
    async def update2(self, ctx):
        client = self.client
        await ctx.message.delete()
        await client.get_channel(827293945003376650).send('__**Giveaway Type Donations:**__\n- `b!gda <@member / id> <amount>` -> <@&785198646731604008>\nThis command allows giveaway managers add to the amount that someone has donated for giveaways\n\n- `b!gdr <@member / id> <amount>` -> <@&785198646731604008>\nThis command allows giveaway managers to remove from someones donated amount\n\n- `gdrs <@member / id>` -><@&785198646731604008>\nThis reset the specified members giveaways donation amount')

    @commands.command()
    async def update3(self, ctx):
        client = self.client
        await ctx.message.delete()
        await client.get_channel(827293945003376650).send('__**Heist Type Donations:**__\n- `b!hda <@member / id> <amount>` -> <@&785631914010214410>\nThis command allows heist managers add to the amount that someone has donated for giveaways\n\n- `b!hdr <@member / id> <amount>` -> <@&785631914010214410>\nThis command allows heist managers to remove from someones donated amount\n\n- `hdrs <@member / id>` -> <@&785631914010214410>\nThis reset the specified members giveaways donation amount')

    @commands.command()
    async def update4(self, ctx):
        client = self.client
        await ctx.message.delete()
        await client.get_channel(827293945003376650).send('__**Event Type Donations:**__\n- `b!eda <@member / id> <amount>` -> <@&791516116710064159>\nThis command allows event managers add to the amount that someone has donated for giveaways\n\n- `b!edr <@member / id> <amount>` -> <@&791516116710064159>\nThis command allows event managers to remove from someones donated amount\n\n- `edrs <@member / id>` -> <@&791516116710064159>\nThis reset the specified members giveaways donation amount')

    @commands.command()
    async def update5(self, ctx):
        client = self.client
        await ctx.message.delete()
        await client.get_channel(827293945003376650).send('If you have any questions to do with anything with this bot feel free to DM <@765322777329664089>\nMore about the bot will be out later sometime!')

def setup(client):
    client.add_cog(Owner(client))