import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Rules
    @commands.command()
    async def rules(self, ctx):
        rules_embed = discord.Embed(title='__**Dank Merchants Rules:**__', description='The Rules Of Dank Merchants', color=0x00ff00)
        rules_embed.add_field(name='Rule One:', value='**Respect all members** of this community. Swearing is allowed but not when you use those words to offend others. Youll be warned for begin toxic in this community.', inline=False)
        rules_embed.add_field(name='Rule Two:', value='**Please keep all drama away.** This can lead to very serious punishments.', inline=False)
        rules_embed.add_field(name='Rule Three:', value='Keep in mind that this is an **English** server and you are expected to use this language appropriately. ', inline=False)
        rules_embed.add_field(name='Rule Four:', value='**Absolutely no NSFW** contents, and do not spam others DM with these contents. This will lead to an immediate ban. ', inline=False)
        rules_embed.add_field(name='Rule Five:', value='**Appropriate contents only**. This includes no disturbing images and hateful speech.', inline=False)
        rules_embed.add_field(name='Rule Six:', value='**Do not ask for personal information** anywhere. This can be extremely irritating to some people.', inline=False)
        rules_embed.add_field(name='Rule Seven:', value='**Do not beg**. Begging of any kind, including begging for promotion, begging for roles, begging for coins, or doing so in peoples DM will result in warn and ban based on the severity of the action.', inline=False)
        rules_embed.add_field(name='Rule Eight:', value='**Do not** advertise or self promote your content anywhere other than #🔗┃self-promo and #🤝🏻┃partner. DM advertising will result in a ban. ', inline=False)
        rules_embed.add_field(name='Rule Nine:', value='**Do not "troll"** — that includes creating "conspiracy theories", asking people to open an unsafe link, and doxxing (revealing ones private information). This can lead to an immediate ban. ', inline=False)
        rules_embed.add_field(name='Rule Ten:', value='**Follow Discord TOS:** https://discord.com/terms', inline=False)
        await ctx.send(embed=rules_embed)

def setup(client):
    client.add_cog(Info(client))