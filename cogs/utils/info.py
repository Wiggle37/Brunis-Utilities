import discord
from discord.ext import commands

from config import *
from checks import *

class Info(commands.Cog, name='info', description='Displays some important info about the server'):

    def __init__(self, bot):
        self.bot = bot

    # Rules
    @commands.command(name='rules', description='Displays the rules of the server')
    @serverChecks.merchants()
    async def rules(self, ctx):
        rules = {
            '__Rule One__': '**Respect all members** of this community. Swearing is allowed but not when you use those words to offend others. You\'ll be warned for being toxic',
            '__Rule Two__': '**Please keep all drama away.** This can lead to very serious punishments.',
            '__Rule Three__:': 'Keep in mind that this is an **English** server and you are expected to use this language appropriately.',
            '__Rule Four__': '**Absolutely no NSFW** content, **DO NOT** send content in dms or any where related to the server as this will lead to a warn or ban',
            '__Rule Five__': '**Appropriate content only**. This includes no disturbing images and hateful speech.',
            '__Rule Six__': '**Do not ask for personal information** anywhere. This can be extremely irritating to some people. And can result in a ban',
            '__Rule Seven__': '**Do not beg**. Begging of any kind, including begging for promotion, begging for roles, begging for coins, or doing so in peoples DM will result in warn and ban based on the severity of the action.',
            '__Rule Eight__': '**Do not** advertise or self promote your content anywhere other than <#787349373448880128> and <#784887859143507978>. DM advertising will result in a warn and after 2 dm ads you will be banned.',
            '__Rule Nine__': '**Do not "troll"** — that includes creating "conspiracy theories", asking people to open an unsafe link, and doxxing (revealing ones private information). This can lead to an immediate ban.',
            '__Rule Ten__': 'A choice is a choice, **DO NOT** argue with a staff over a warn for this will only get you another warn.',
            '__Rule Eleven__': '**DO NOT** mini-mod dont pretend like you are a mod that makes other stff members like they are not doing a good enough job',
            '__Rule Twelve__': '**Follow Discord TOS:** https://discord.com/terms'
        }
        msg = ''
        for num, rule in rules.items():
            msg += f'**{num}** ➞ {rule}\n\n'

        rules_embed = discord.Embed(title='__**Dank Merchants Rules:**__', description=msg, color=0x00ff00)
        rules_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=rules_embed)

    # Dank Rules
    @commands.command(name='dankrules', description='Displays the rules of Dank Memer')
    @serverChecks.merchants()
    async def dankrules(self, ctx):
        rules = {
            '__Rule One__\nUser-bots, Spamming and Macros': 'Usage of user-bots, macros, scripts, auto-typers or anything else enabling automation of commands is strictly forbidden. In addition to this, massive amounts of spam is not allowed and will be punished with equal severity.',
            '__Rule Two__\nSharing Exploits': 'Sharing exploits or exploitative bugs with other users is forbidden. Please report all exploits and bugs to staff on the [Dank Memer Support Server](https://discord.com/invite/meme) so that we can fix it as soon as possible.',
            '__Rule Three__\nGiveaway Requirements or Bot Usage Requirements in Your Server': 'You should not lock the bot, or giveaways for the bot, behind paywalls. This means stuff like patreon roles, donor roles (with irl money), etc, is forbidden for giveaway requirements or role locks. The only exception to this is boosters',
            '__Rule Four__\nRacism, Homophobia, Sexism or Slurs': 'None of the above will be tolerated through usage of Dank Memer. We will not punish you for what you say outside of the usage of our commands. Evidence found of this done through our commands will result in punishment.',
            '__Rule Five__\nAdvertisement':'Usage of Dank Memer to advertise or promote anything will result in a punishment. This includes other Discord servers. Giving our currency in exchange for invites to your server is also forbidden.',
            '__Rule Six__\nReal Money Trading': 'Dank Memers currency is not to be traded for real money or discord nitro. Buying anything with real money outside of our patreon and website, will get you a ban.',
            '__Rule Seven__\nEtiquette': 'Starting harmful rumors about the bot, causing unnecessary drama within our servers about the bot, or witch hunting staff members are all ban worthy behaviors.',
            '__Rule Eight__\nDiscord Terms of Service and Usage Guidelines': 'Through Dank Memer you agree to the Dank Member rules and Discord rules'
        }
        msg = ''
        for num, rule in rules.items():
            msg += f'**{num}** ➞ {rule}\n\n'

        dank_rules = discord.Embed(title='Dank Memer Rules', description=msg, color=0x00ff00)
        dank_rules.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=dank_rules)

    # Warning Policy
    @commands.command(name='warningpolicy', description='The warning policy in the server')
    @serverChecks.merchants()
    async def warnp(self, ctx):
        warns = {
            '__First Warning__': 'Nothing',
            '__First Warning__': 'Nothing',
            '__Third Warning__': 'Nothing',
            '__Forth Warning__': 'Nothing',
            '__Fifth Warning__': '2 hour mute',
            '__Sixth Warning__': '6 hour mute',
            '__Seventh Warning__': '12 hour mute',
            '__Eaith Warning__': '24 hour mute',
            '__Ninth Warning__': '48 hour mute',
            '__Tenth Warning__': 'Ban',
        }
        msg = ''
        for num, pun in warns.items():
            msg += f'**{num}** ➞ {pun}\n\n'
        warn_embed = discord.Embed(title='__**Dank Merchants Warning Policy:**__', description=msg, color=0x00ff00)
        warn_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=warn_embed)

    # Trading Rules
    @commands.command(name='tradingrules', description='The rule of trading for the server')
    @serverChecks.merchants()
    async def traderules(self, ctx):
        rules = {
            '__Rule One__': 'If you want to trade, post your ads at <#785645266790252554>. Inappropriate and out-of-place ads will be removed.',
            '__Rule Two__': 'If you want to request a trade, go to <#787393772711051324>. Do not post ads here otherwise you will receiving a warning.',
            '__Rule Three__': 'Trade only in the 3 trading channels. If seen trading in other channels you will get a warn.',
            '__Rule Four__': 'Do not "troll" your seller or buyer, that includes agreeing to trade at first and then tell him/her that you changed your mind on purpose.',
            '__Rule Five__': 'If you got scammed, report them at <#787761394664996865>.',
            '__Rule Six': 'If a trade was satisfactory you should vouch for them at <#815057225378431056>. No farming vouches by trading for 1 pink the trade value has to be at least 500k for a vouch.'
        }
        msg = ''
        for num, rule in rules.items:
            msg += f'**{num}** ➞ {rule}\n'
        traderules_embed = discord.Embed(title='__**Dank Merchants Trading Rules:**__', description=msg, color=0x00ff00)
        traderules_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=traderules_embed)

    # Giveaway Rules
    @commands.command(name='giveawayrules', description='The rules for giveaways for the server')
    @serverChecks.merchants()
    async def gawrules(self, ctx):
        rules = {
            '__Rule One__': 'Only level amari 2s may claim giveaway prizes to avoid freeloaders.',
            '__Rule Two__': 'You may use **<@&810249131988746260>** to skip the requirements of an exclusive giveaway.',
            '__Rule Three__': 'If you didnt receive your prize in 12 hours go to <#787761394664996865> and ask for help, **DO NOT** dm the gaw manager that hosted the giveaway',
            '__Rule Four__': 'You are not allowed to use secondary accounts (or alts) as this is unfair to others. Alts will be immediately banned.',
            '__Rule Five__': 'If you are level 2 and stopped talking/only camp in giveaway channels, you will not receive the prize. Thats no different from a freeloader.',
            '__Rule Six__': 'If you dm a giveaway manager **at all** about your prize they have the rights to either reroll the giveaway or keep the prize for themeselves'
        }
        msg = ''
        for num, rule in rules.items():
            msg += f'**{num}** ➞ {rule}\n'
        gaw_embed = discord.Embed(title='__**Dank Merchants Giveaway Rules:**__', description=msg, color=0x00ff00)
        gaw_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=gaw_embed)

    # Special Roles
    @commands.command(name='specialroles', description='The info for special roles in the server')
    @serverChecks.merchants()
    async def specroles(self, ctx):
        roles = {
            '__Member Of The Week__': '<@&786610856158429204> - Get hoisted just below staff followed by a week of premium. The person who sends the most messages in a week gets this role.',
            '__Top 3 Weekly__': '<@&800496416178700288>\nThis is awarded to the three most active members every week. Top 3 finishers can bypass ALL giveaways!',
            '__Premium__': '<@&787734881563705354> - Premium users have this, and you can get this by doing various different things.',
            '__Server Suporter__': '<@&785344908374310912> - Do `-vote` in <#784492719564652544> and vote for us on top.gg every 12 hours! You get this special role, access to <#787352130448523264>.',
            '__Bot Master__': '<@&787731701220376586> - Be the most active bot player and you may request to obtain this role!',
            '__Lucky ASF__': '<@&788738302164467734> - Win 6 lottery events to obtain this role!',
            '__Bumping God__': '<@&787868761620348929> - Be the most active member in <#784994978661138453>',
            '__Server Booster__': '<@&797486130844663829>\nBoost our server to receive this role',
            '__Investor__': '<@&799844367501099028>\nMake any of our bots premium to receive this role',
        }
        msg = ''
        for num, role in roles.items():
            msg += f'**{num}** ➞ {role}\n'
        specroles_embed = discord.Embed(title='__**Dank Merchants Special Roles:**__', description=msg, color=0x00ff00)
        specroles_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=specroles_embed)

    # Exclusive Roles
    @commands.command(name='exclusiveroles', description='Info on some of the most rare roles in the server')
    @serverChecks.merchants()
    async def eroles(self, ctx):
        roles = {
            '__Dank Harbor Verteran__': '<@&784560843890753577> - For those who survived Dank Harbor',
            '__Server Bot Developer:__': '<@&788738308879941633> - Develop a bot for the server',
            '__Christmas 2020__': '<@&791229305320767510> - For those who were around in Chrismas 2020',
            '__1k Special Winner__': '<@&807824584396767292> - For those that won in 1k special event',
            '__Highest Donor__': '<@&793189820151234620> - Highest donor gets their own custom channel'
        }
        msg = ''
        for num, role in roles.items():
            msg += f'**{num}** ➞ {role}\n'
        eroles_embed = discord.Embed(title='__**Dank Merchants Exclusive Roles:**__', description=msg, color=0x00ff00)
        eroles_embed.set_footer(text='Last updated: 6/22/21')
        await ctx.send(embed=eroles_embed)

    # Donations
    @commands.command(name='donationperks', description='Info on the donation perks')
    @serverChecks.merchants()
    async def donoperks(self, ctx):
        donos = {
            '__5 Million Donor__': '<@&787342154862166046> - Access to exclusive giveaways/heists',
            '__10 Million Donor__': '<@&787342156573704203> - Access to <#787349373448880128>',
            '__25 Million Donor__': '<@&799022090791419954> - Unlock <#788159178865639511> and a list of robbing servers',
            '__50 Million Donor__': '<@&787868761528336427> - Access to Dyno `?afk` and Dank Memer `pls snipe`',
            '__100 Million Donor__': '<@&787868759720722493> - Access to <#800386641839390720>',
            '__250 Million Donor__': '<@&799844364389187616> - Access to <#788160596319272980> and carl highlight command',
            '__500 Million Donor__': '<@&799022083778543696> - Reaction perms in all trading channels + 2 weeks premium',
            '__1 Billion Donor__': '<@&799844367551692827> - Exclusive **custom command** made only for you!',
            '__2.5 Billlion Donor__': '<@&824615522934849607> - Ability to **BYPASS ALL** giveaways server-wide!',
            '__5 Billion Donor__': 'Fancy letter autoresponse when name is pinged',
            '__🤑 Highest Donor 🤑__': '<@&793189820151234620> - Your **OWN** Dank channel + auto reaction when pinged!'
        }
        msg = ''
        for num, role in donos.items():
            msg += f'**{num}** ➞ {role}\n'
        donor_embed = discord.Embed(title='__**Dank Merchants Donation Perks:**__', description=msg, color=0x00ff00)
        donor_embed.set_footer(text='Last updated: 6/23/21')
        await ctx.send(embed=donor_embed)

    # Invites
    @commands.command(name='inviteperks', description='The perks you get for inviting people in the server')
    @serverChecks.merchants()
    async def invperks(self, ctx):
        perks = {
            '__2 Invites__': '<@&787342156611321857> - Access to nitro giveaways',
            '__5 Invites__': '<@&787342156846727188> - Ability to add reaction to giveaways and access to <#854916429185941535>',
            '__10 Invites__': '<@&787348338004590612> - Guild wide ability to embed links',
            '__15 Invites__': '<@&787348339733168179> - Dyno `?afk` access',
            '__30 Invites__': '<@&787348339791233045> - 6 months server premium'
        }
        msg = ''
        for num, role in perks.items():
            msg += f'**{num}** ➞ {role}\n'
        inv_embed = discord.Embed(title='__**Dank Merchants Invite Perks:**__', description=msg, color=0x00ff00)
        inv_embed.set_footer(text='Last updated: 6/23/21')
        await ctx.send(embed=inv_embed)

    # Levels
    @commands.command(name='levelperks', description='The servers leveling perks')
    @serverChecks.merchants()
    async def lvlperks(self, ctx):
        level = {
            '__Level 5__': '<@&785676777585639464> - `pls weekly/monthly` access',
            '__Level 10__': '<@&785725155561308171> - Unlock all color roles [here](https://discord.com/channels/784491141022220309/784547669619507201/805984931707617330)',
            '__Level 15__': '<@&785676889736871946> - All channel reaction perms',
            '__Level 20__': '<@&785725154373271594> - Guild wide image permissions',
            '__Level 30 __': '<@&785676961904852992> - Access to `;;snipe`',
            '__Level 40__': '<@&785676992481329182> - Free 10 days of server premium',
            '__Level 50__': '<@&785726480092626945> - Ability to send links',
            '__Level 69__': '<@&799844364976259082> - The "<a:pepeeggplant:828020469286436864>" emote reaction when you are pinged!',
            '__Level 100__': '<@&810249129909420122> - Access to carl bot\'s highlight (cmd is *hl) to highlight anything in the server and receive an exclusive color role from the past (contact me). If you reach here, You are truly a god!'
        }
        msg = ''
        for num, perk in level.items():
            msg += f'**{num}** ➞ {perk}\n'
        lvl_embed = discord.Embed(title='__**Dank Merchants Level Perks:**__', description=msg, color=0x00ff00)
        await ctx.send(embed=lvl_embed)

    # Booster Perks
    @commands.command(name='boosterperks', description='The amazing perks of being a server booster')
    @serverChecks.merchants()
    async def booster(self, ctx):
        inv_embed = discord.Embed(title='__**Dank Merchants Booster Perks:**__', description='The Booster Perks Of Dank Merchants', color=0xf47fff)
        inv_embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/757131348539473920.gif?v=1')
        inv_embed.add_field(name='__Single Booster Perks:__', value='<@&797486130844663829>\n<a:shiny_boost:802975176194129950> Receive all <@&787734881563705354> perks as long as your boost lasts\n<a:shiny_boost:802975176194129950> `pls snipe` and `?afk` access\n<a:shiny_boost:802975176194129950> Bypass all giveaways\n<a:shiny_boost:802975176194129950> Your own auto-response in animated letters\n<a:shiny_boost:802975176194129950> Access to exclusive <#801287649309884447>\n<a:shiny_boost:802975176194129950> All boosters are pinged in silent giveaways', inline=False)
        inv_embed.add_field(name='__Double Booster Perks:__', value='<@&786610856308768768>\n<a:Boost:800379805367402496> Your own dank memer channel (can invite up to 5 friends)\n<a:Boost:800379805367402496> 6 hour claim time for nitro giveaways (normies get 10 minutes)\n<a:Boost:800379805367402496> `pls esnipe` access\n<a:Boost:800379805367402496> List of robbing servers\n<a:Boost:800379805367402496> Auto reaction when your name is pingedn\n<a:Boost:800379805367402496> Carl-bot `*hl` access (when key word is said in chat youll be notified)\n<a:Boost:800379805367402496> booster perks last one more week if you boost a whole month', inline=False)
        inv_embed.add_field(name='__Multi Booster Perks:__', value='<@&797486130844663829>\n<a:NR_Boost:800379946647420989> Custom trigger\n<a:NR_Boost:800379946647420989> Up to 10 friends can join you in your private channel\n<a:NR_Boost:800379946647420989> Add two emotes of your choice to the server\n <a:NR_Boost:800379946647420989> Promote your content in <#784887859143507978> with <@&785930653665067038> ping\n<a:NR_Boost:800379946647420989> Booster perks last two more weeks if you boost a whole month', inline=False)
        inv_embed.set_footer(text='Last updated: 6/23/21')
        await ctx.send(embed=inv_embed)

def setup(bot):
    bot.add_cog(Info(bot))