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
        rules_embed.add_field(name='__Rule Eleven:__', value='**DO NOT** beg for money this will only get you a warn', inline=False)
        rules_embed.add_field(name='__Rule Twelve:__', value='A choice is a choice, **DO NOT** argue with a mod/admin over a warn for this will only get you another warn', inline=False)
        rules_embed.add_field(name='__Note:__', value='*By verifying you agree to every term & condition listed above.*')
        await ctx.send(embed=rules_embed)

    #Dank Rules
    @commands.command()
    async def dankrules(self, ctx):
        dank_rules = discord.Embed(title='Dank Memer Rules', description='https://dankmemer.lol/rules', color=0x00ff00)
        dank_rules.add_field(name='__Rule One__\n**User-bots, Spamming and Macros**', value='\nUsage of user-bots, macros, scripts, auto-typers or anything else enabling automation of commands is strictly forbidden. In addition to this, massive amounts of spam is not allowed and will be punished with equal severity.', inline=False)
        dank_rules.add_field(name='__Rule Two__\n**Sharing Exploits**', value='Sharing exploits or exploitative bugs with other users is forbidden. Please report all exploits and bugs to staff on the [Dank Memer Support Server](https://discord.com/invite/meme) so that we can fix it as soon as possible.', inline=False)
        dank_rules.add_field(name='__Rule Three__\n**Giveaway Requirements or Bot Usage Requirements in Your Server**', value='You should not lock the bot, or giveaways for the bot, behind paywalls. This means stuff like patreon roles, donor roles (with irl money), etc, is forbidden for giveaway requirements or role locks. The only exception to this is boosters, we will allow you to lock things behind being a booster for your server. Things like level locks using external bots is perfectly fine.', inline=False)
        dank_rules.add_field(name='__Rule Four__\n**Racism, Homophobia, Sexism or Slurs**', value='None of the above will be tolerated through usage of Dank Memer. We will not punish you for what you say outside of the usage of our commands. Evidence found of this done through our commands will result in punishment.', inline=False)
        dank_rules.add_field(name='__Rule Five__\n**Advertisement**', value='Usage of Dank Memer to advertise or promote anything will result in a punishment. This includes other Discord servers. Giving our currency in exchange for invites to your server is also forbidden.', inline=False)
        dank_rules.add_field(name='__Rule Six__\n**Real Money Trading**', value='Dank Memers currency is not to be traded for real money or discord nitro. Buying anything with real money outside of our patreon and website, will get you a ban.', inline=False)
        dank_rules.add_field(name='__Rule Seven__\n**Etiquette**', value='Starting harmful rumors about the bot, causing unnecessary drama within our servers about the bot, or witch hunting staff members are all ban worthy behaviors.', inline=False)
        dank_rules.add_field(name='__Rule Eight__\n**Discord Terms of Service and Usage Guidelines**', value='Through usage of Dank Memer, you accept [Dank Memer Terms of Service](https://dankmemer.lol/terms) and [Privacy Policy](https://dankmemer.lol/privacy). Additionally, you accept [Discords Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines), these of which are enforceable through Dank Memer.')
        await ctx.send(embed=dank_rules)

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
        await ctx.send(embed=traderules_embed)

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
        specroles_embed = discord.Embed(title='__**Dank Merchants Special Roles:**__', description='The Special Roles Of Dank Merchants', color=0x00ff00)
        specroles_embed.add_field(name='__Member Of The Week:__', value='<@&786610856158429204>\nBe the highest hoisted member (higher than owner) in the server followed by a week of premium. The person who sends the most messages in a week gets this role.', inline=False)
        specroles_embed.add_field(name='__Premium:__', value='Premium users have this', inline=False)
        specroles_embed.add_field(name='__Trusted Trader:__', value='<@&787731702755754014>\nWith level 10 and 60 vouches, you may request to obtain this role to be more trusted in trades and gain reaction perms in trading channels as well as access to <#788864230220103780> and <#788864304786047026>', inline=False)
        specroles_embed.add_field(name='__Trusted Middle Man:__', value='<@&797676814452391936>\nTo get this role you must have trusted trader role and level 20', inline=False)
        specroles_embed.add_field(name='__Top Rated Trader:__', value='<@&797676814452391936>\nTo get this role get 120 vouches and level 20', inline=False)
        specroles_embed.add_field(name='__Server Suporter:__', value='<@&785344908374310912>\nDo `-vote` in <#784492719564652544> and vote for us on top.gg every 12 hours! You get this special role, access to <#787352130448523264>', inline=False)
        specroles_embed.add_field(name='__Bot Master:__', value='<@&787731701220376586>\nBe the most active bot player and you may request to obtain this role!', inline=False)
        specroles_embed.add_field(name='__Lucky ASF:__', value='<@&788738302164467734>\nWin 6 lottery events to obtain this role!', inline=False)
        specroles_embed.add_field(name='__Bumping God:__', value='<@&787868761620348929>\nBe the most active member in <#784994978661138453>', inline=False)
        specroles_embed.add_field(name='__Server Booster:__', value='<@&797486130844663829>\nBoost our server to receive this role', inline=False)
        specroles_embed.add_field(name='__Investor:__', value='<@&799844367501099028>\nMake any of our bots premium to receive this role', inline=False)
        specroles_embed.add_field(name='__Top 3 Weekly:__', value='<@&800496416178700288>\nThis is awarded to the three most active members every week. Top 3 finishers can bypass ALL giveaways!', inline=False)
        await ctx.send(embed=specroles_embed)

    #Exlusive Roles
    @commands.command()
    async def eroles(self, ctx):
        eroles_embed = discord.Embed(title='__**Dank Merchants Exlusive Roles:**__', description='The Exlusive Roles Of Dank Merchants', color=0x00ff00)
        eroles_embed.add_field(name='__Dank Harbor Veteran:__', value='<@&784560843890753577>\nFor those who survived Dank Harbor', inline=False)
        eroles_embed.add_field(name='__Server Bot Developer:__', value='<@&788738308879941633>\nDevelope a bot for the server(already taken by <@765322777329664089>)', inline=False)
        eroles_embed.add_field(name='__Christmas 2020:__', value='<@&791229305320767510>\nFor those who won in Chrismas 2020', inline=False)
        eroles_embed.add_field(name='__1000 Special Winner:__', value='<@&807824584396767292>\nFor those thay own in 1k special event', inline=False)
        eroles_embed.add_field(name='__Highest Donor:__', value='<@&793189820151234620>\nHighest donor gets their own custom channel', inline=False)
        await ctx.send(embed=eroles_embed)

    #Donations
    @commands.command()
    async def donoperks(self, ctx):
        donor_embed = discord.Embed(title='__**Dank Merchants Donation Perks:**__', description='The Donations Perks Of Dank Merchants', color=0x00ff00)
        donor_embed.add_field(name='__5 Million Donor:__', value='<@&787342154862166046>\nAccess to exclusive giveaways/heists', inline=False)
        donor_embed.add_field(name='__10 Million Donor:__', value='<@&787342156573704203>\nAccess to <#787349373448880128>', inline=False)
        donor_embed.add_field(name='__25 Million Donor:__', value='<@&799022090791419954>\nUnlock <#788159178865639511> and a list of robbing servers', inline=False)
        donor_embed.add_field(name='__50 Million Donor:__', value='<@&787868761528336427>\nAccess to Dyno `?afk` and Dank Memer `pls snipe` ', inline=False)
        donor_embed.add_field(name='__100 Million Donor:__', value='<@&787868759720722493>\nAccess to <#800386641839390720>', inline=False)
        donor_embed.add_field(name='__250 Million Donor:__', value='<@&799844364389187616>\nAccess to <#788160596319272980> and carl highlight command', inline=False)
        donor_embed.add_field(name='__500 Million Donor:__', value='<@&799022083778543696>\nReaction perms in all trading channels + 2 weeks premium', inline=False)
        donor_embed.add_field(name='__1 Billion Donor:__', value='<@&799844367551692827>\nExclusive **custom command** made only for you!', inline=False)
        donor_embed.add_field(name='__2.5 Billion Donor:__', value='<@&824615522934849607>\nAbility to **BYPASS ALL** giveaways server-wide!', inline=False)
        donor_embed.add_field(name='__Highest Donor:__', value='<@&793189820151234620>\nYour **OWN** Dank channel + auto reaction when pinged!', inline=False)
        await ctx.send(embed=donor_embed)

    #Invites
    @commands.command()
    async def invperks(self, ctx):
        inv_embed = discord.Embed(title='__**Dank Merchants Invite Perks:**__', description='The Invite Perks Of Dank Merchants', color=0x00ff00)
        inv_embed.add_field(name='__2 Invites:__', value='<@&787342156611321857>\nGain access to some inviter-exclusive giveaways', inline=False)
        inv_embed.add_field(name='__5 Invites:__', value='<@&787342156846727188>\nAbility to add reactions in giveaway channels and unlock <#787349373448880128>', inline=False)
        inv_embed.add_field(name='__10 Invites:__', value='<@&787348338004590612>\nGuild-wide ability to embed links ', inline=False)
        inv_embed.add_field(name='__15 Invites:__', value='<@&787348339733168179>\nAdvertise your server in <#784887859143507978> with <@&785930653665067038> ping and Dyno ?afk access', inline=False)
        inv_embed.add_field(name='__30 Invites:__', value='<@&787348339791233045>\nLife time exclusive giveaway pass + your private text and voice channel (can invite 3 friends) and 1 month premium', inline=False)
        inv_embed.add_field(name='__75+ Invites:__', value='<@&787348341675393025>\n**LIFE TIME PREMIUM**', inline=False)
        await ctx.send(embed=inv_embed)

    #Levels
    @commands.command()
    async def lvlperks(self, ctx):
        lvl_embed = discord.Embed(title='__**Dank Merchants Level Perks:**__', description='The Level Perks Of Dank Merchants', color=0x00ff00)
        lvl_embed.add_field(name='__Level 5:__', value='<@&785676777585639464>\n`pls weekly/monthly` access', inline=False)
        lvl_embed.add_field(name='__Level 10:__', value='<@&785725155561308171>\nUnlock all color roles at <#784547669619507201>', inline=False)
        lvl_embed.add_field(name='__Level 15:__', value='<@&785676889736871946>\nAll channels Reaction perms', inline=False)
        lvl_embed.add_field(name='__Level 20:__', value='<@&785725154373271594>\nGuild-wide image perms', inline=False)
        lvl_embed.add_field(name='__Level 25:__', value='<@&785725155762372608>\nAbility to embed links and unlock <#787352549622546464>', inline=False)
        lvl_embed.add_field(name='__Level 30:__', value='<@&785676961904852992>\n`pls snipe` access and 1 week of premium', inline=False)
        lvl_embed.add_field(name='__Level 40:__', value='<@&785676992481329182>\nAbility to upload an emote of your choice(no NSFW) ', inline=False)
        lvl_embed.add_field(name='__Level 50:__', value='<@&785726480092626945>\nCustom role with color of your choice', inline=False)
        lvl_embed.add_field(name='__Level 69:__', value='<@&799844364976259082>\nThe "<a:pepeeggplant:828020469286436864>" emote reaction when you are pinged!', inline=False)
        await ctx.send(embed=lvl_embed)

    #Booster Perks
    @commands.command()
    async def booster(self, ctx):
        inv_embed = discord.Embed(title='__**Dank Merchants Booster Perks:**__', description='The Booster Perks Of Dank Merchants', color=0xf47fff)
        inv_embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/757131348539473920.gif?v=1')
        inv_embed.add_field(name='__Single Booster Perks:__', value='<@&797486130844663829>\n<a:shiny_boost:802975176194129950> Receive all <@&787734881563705354> perks as long as your boost lasts\n<a:shiny_boost:802975176194129950> `pls snipe` and `?afk` access\n<a:shiny_boost:802975176194129950> Bypass all giveaways\n<a:shiny_boost:802975176194129950> Your own auto-response in animated letters\n<a:shiny_boost:802975176194129950> Access to exclusive <#801287649309884447>\n<a:shiny_boost:802975176194129950> All boosters are pinged in silent giveaways', inline=False)
        inv_embed.add_field(name='__Double Booster Perks:__', value='<@&786610856308768768>\n<a:Boost:800379805367402496> Your own dank memer channel (can invite up to 5 friends)\n<a:Boost:800379805367402496> 6 hour claim time for nitro giveaways (normies get 10 minutes)\n<a:Boost:800379805367402496> `pls esnipe` access\n<a:Boost:800379805367402496> List of robbing servers\n<a:Boost:800379805367402496> Auto reaction when your name is pingedn\n<a:Boost:800379805367402496> Carl-bot `*hl` access (when key word is said in chat youll be notified)\n<a:Boost:800379805367402496> booster perks last one more week if you boost a whole month', inline=False)
        inv_embed.add_field(name='__Multi Booster Perks:__', value='<@&797486130844663829>\n<a:NR_Boost:800379946647420989> Custom trigger\n<a:NR_Boost:800379946647420989> Up to 10 friends can join you in your private channel\n<a:NR_Boost:800379946647420989> Add two emotes of your choice to the server\n <a:NR_Boost:800379946647420989> Promote your content in <#784887859143507978> with <@&785930653665067038> ping\n<a:NR_Boost:800379946647420989> Booster perks last two more weeks if you boost a whole month', inline=False)
        await ctx.send(embed=inv_embed)

def setup(client):
    client.add_cog(Info(client))