import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Rules
    @commands.command()
    async def rules(self, ctx):
        rules_embed = discord.Embed(title='__**Dank Merchants Rules:**__', description='The Rules Of Dank Merchants', color=0x00ff00)
        rules_embed.add_field(name='__Rule One:__', value='**Respect all members** of this community. Swearing is allowed but not when you use those words to offend others. Youll be warned for begin toxic in this community.', inline=False)
        rules_embed.add_field(name='__Rule Two:__', value='**Please keep all drama away.** This can lead to very serious punishments.', inline=False)
        rules_embed.add_field(name='__Rule Three:__', value='Keep in mind that this is an **English** server and you are expected to use this language appropriately.', inline=False)
        rules_embed.add_field(name='__Rule Four:__', value='**Absolutely no NSFW** contents, and do not spam others DM with these contents. This will lead to an immediate ban. ', inline=False)
        rules_embed.add_field(name='__Rule Five:__', value='**Appropriate contents only**. This includes no disturbing images and hateful speech.', inline=False)
        rules_embed.add_field(name='__Rule Six:__', value='**Do not ask for personal information** anywhere. This can be extremely irritating to some people.', inline=False)
        rules_embed.add_field(name='__Rule Seven:__', value='**Do not beg**. Begging of any kind, including begging for promotion, begging for roles, begging for coins, or doing so in peoples DM will result in warn and ban based on the severity of the action.', inline=False)
        rules_embed.add_field(name='__Rule Eight:__', value='**Do not** advertise or self promote your content anywhere other than <#787349373448880128> and <#784887859143507978>. DM advertising will result in a ban. ', inline=False)
        rules_embed.add_field(name='__Rule Nine:__', value='**Do not "troll"** — that includes creating "conspiracy theories", asking people to open an unsafe link, and doxxing (revealing ones private information). This can lead to an immediate ban. ', inline=False)
        rules_embed.add_field(name='__Rule Ten:__', value='**Follow Discord TOS:** https://discord.com/terms', inline=False)
        rules_embed.add_field(name='__Note:__', value='*By verifying you agree to every term & condition listed above.*')
        await ctx.send(embed=rules_embed)

    #Warning Policy
    @commands.command()
    async def warnp(self, ctx):
        warn_embed = discord.Embed(title='__**Dank Merchants Warning Policy:**__', description='The Warning Policy Of Dank Merchants', color=0x00ff00)
        warn_embed.add_field(name='__First Warning:__', value='Nothing', inline=False)
        warn_embed.add_field(name='__Second Warning:__', value='Nothing', inline=False)
        warn_embed.add_field(name='__Third Warning:__', value='Nothing', inline=False)
        warn_embed.add_field(name='__Forth Warning:__', value='3 hour mute', inline=False)
        warn_embed.add_field(name='__Fifth Warning:__', value='12 hour mute', inline=False)
        warn_embed.add_field(name='__Sixth Warning:__', value='1 day temperary ban', inline=False)
        warn_embed.add_field(name='__Seventh Warning:__', value='7 day temperary ban', inline=False)
        warn_embed.add_field(name='__Eighth Warning:__', value='Permanent ban', inline=False)
        warn_embed.add_field(name='__Note:__', value='Warns can be cleared if one does not receive any more warnings in 30 days. Also, depending on the severity of the case, one can be immediately banned without having 6-8 warnings. The moderator holds the final decision.')
        await ctx.send(embed=warn_embed)

    #Trading Rules
    @commands.command()
    async def traderules(self, ctx):
        traderules_embed = discord.Embed(title='__**Dank Merchants Trading Rules:**__', description='The Rules Of Trading In Dank Merchants', color=0x00ff00)
        traderules_embed.add_field(name='__Rule One:__', value='If you want to trade, post your ads at <#785645266790252554>. Inappropriate and out-of-place ads will be removed.', inline=False)
        traderules_embed.add_field(name='__Rule Two:__', value='If you want to request a trade, go to <#787393772711051324>. Do not post ads here otherwise you will receiving a warning.', inline=False)
        traderules_embed.add_field(name='__Rule Three:__', value='Trade only in the 3 trading channels.', inline=False)
        traderules_embed.add_field(name='__Rule Four:__', value='Do not "troll" your seller or buyer, that includes agreeing to trade at first and then tell him/her that you changed your mind on purpose.', inline=False)
        traderules_embed.add_field(name='__Rule Five:__', value='If you got scammed, report them at <#787761394664996865>', inline=False)
        traderules_embed.add_field(name='__Rule Six:__', value='If a trade was satisfactory you should vouch for them at <#815057225378431056>', inline=False)
        await ctx.send(embed=warn_embed)

    #Giveaway Rules
    @commands.command()
    async def gawrules(self, ctx):
        traderules_embed = discord.Embed(title='__**Dank Merchants Trading Rules:**__', description='The Rules Of Trading In Dank Merchants', color=0x00ff00)
        traderules_embed.add_field(name='__Rule One:__', value='Only level amari 2s may claim giveaway prizes to avoid freeloaders.', inline=False)
        traderules_embed.add_field(name='__Rule Two:__', value='You may use **giveaway pass** to skip the requirements of an exclusive giveaway.', inline=False)
        traderules_embed.add_field(name='__Rule Three:__', value='If you didnt receive your prize in 2 hours go to <#787761394664996865> and ask for help', inline=False)
        traderules_embed.add_field(name='__Rule Four:__', value='You are not allowed to use secondary accounts (or alts) as this is unfair to others. Alts will be immediately banned.', inline=False)
        traderules_embed.add_field(name='__Rule Five:__', value='If you are level 2 and stopped talking/only camp in giveaway channels, you will not receive the prize. Thats no different from a freeloader.', inline=False)
        await ctx.send(embed=traderules_embed)

    #Special Roles
    @commands.command()
    async def specroles(self, ctx):
        specroles_embed = discord.Embed(title='__**Dank Merchants Special Roles:**__', description='The Special Roles Of Dank Merchants And How To Obtain Them', color=0x00ff00)
        specroles_embed.add_field(name='<@&786610856158429204>', value='Be the highest hoisted member (higher than owner) in the server followed by a week of premium. The person who sends the most messages in a week gets this role.', inline=False)
        specroles_embed.add_field(name='<@&787731702755754014>', value='With level 10 and 60 vouches, you may request to obtain this role to be more trusted in trades and gain reaction perms in trading channels as well as access to <#788864230220103780> and <#788864304786047026>', inline=False)
        specroles_embed.add_field(name='<@&797676814452391936>', value='To get this role you must have trusted trader role and level 20', inline=False)
        specroles_embed.add_field(name='<@&797676814452391936>', value='To get this role get 120 vouches and level 20', inline=False)
        specroles_embed.add_field(name='<@&785344908374310912>', value='Do `-vote` in <#784492719564652544> and vote for us on top.gg every 12 hours! You get this special role, access to <#787352130448523264>', inline=False)
        specroles_embed.add_field(name='<@&787731701220376586>', value='Be the most active bot player and you may request to obtain this role!', inline=False)
        specroles_embed.add_field(name='<@&788738302164467734>', value='Win 6 lottery events to obtain this role!', inline=False)
        specroles_embed.add_field(name='<@&787868761620348929>', value='Be the most active member in <#784994978661138453>', inline=False)
        specroles_embed.add_field(name='<@&797486130844663829>', value='Boost our server to receive this role, scroll down for perks', inline=False)
        specroles_embed.add_field(name='<@&799844367501099028>', value='Make any of our bots premium to receive this role', inline=False)
        specroles_embed.add_field(name='<@&800496416178700288>', value='This is awarded to the three most active members every week. Top 3 finishers can bypass ALL giveaways!', inline=False)
        await ctx.send(embed=specroles_embed)

def setup(client):
    client.add_cog(Info(client))