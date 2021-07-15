import discord
from discord.ext import commands
import sqlite3

channels = [
            784491141022220312, # General

            785645266790252554, # Selling Ads
            787393772711051324, # Buying Ads
            827650976840155206, # Dueling Ads
            788864230220103780, # Secure Ads
            788864304786047026, # Secure Trading
            785316826983825418, # Trading 1
            787762140668756008, # Trading 2
            824096045154959381, # Trading 3
            815057225378431056, # Vouch

            784492608368934952, # Dank Memer 1
            784492642540191764, # Dank Memer 2
            789139093124153397, # Dank Memer 3
            826920379179466763, # Dank Memer 4
            787352130448523264, # Voter Dank Memer
            800386641839390720, # Donor Dank Memer
            789129362016436234, # Duel Arena 1
            789129584795975720, # Dual Arena 2
            808197857664434216, # Flex Zone

            787352549622546464, # Premium Chat
            800378397992943646, # Premium Dank Memer 1
            800378442910400583, # Premium Dank Memer 2
            785154861922254848, # Giveaway Donations
            818269054103978004, # Heist Donations

            784494364754706462, # Events
            850526312865988638, # Mafia Join

            848283586372042752, # Scibowl Practice
            784536730702970891, # Mudae
            792522447516860427, # Gambling Bot
            792522332773548112, # Virtual Fisher
            784537913131270156, # Pokemon Spawn
            784539206479380502, # Marrige Hall
            784541575208239105, # Mining Cave

            834797455262482492, # Homework Help
            787349373448880128, # Self-Promo
            784996713198911538, # Counting
            788842455671767110, # One Word Story
            787350455998087178, # Auto Memes
            784494535139917874, # Media

            785216538201817130, # Giveaway Create
            784498929714462740, # Staff Chat
            805620755446366280, # Moderate Here
            784529738491625473, # Goodbye

            826895397434687558, # Team Dank Memer 1
            829510480233103390, # Team Dank Memer 2
            826895495481524245, # Team Dank Memer 3
            826896092993945650, # Send Money To Duke For Daily Heists
            826897659474214974, # Contribution Reports
            826898057424797726, # Contribution Notes
        ]

class economysettings:
    @staticmethod
    def banned(user_id):
        dbase = sqlite3.connect('settings.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT ban FROM bans WHERE user_id = '{user_id}'")
        result = cursor.fetchone()

        dbase.close()
        return result is not None

    @staticmethod
    def economycheck():
        async def predicate(ctx):
            return ctx.channel.id not in channels \
                and economysettings.banned(ctx.author.id) is None
        return commands.check(predicate)

class heistmode:
    def heist():
        dbase = sqlite3.connect('settings.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT heistmode FROM heistmode")
        result = cursor.fetchone()

        if result is None:
            return False

        elif result[0] == 'True':
            return True

        elif result[0] == 'False':
            return False