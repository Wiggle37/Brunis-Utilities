import discord
import sqlite3

### - - - - - Levels - - - - - ###
class levels:
    name = None
    level = None
    role_id = None
    emoji = None

class level5(levels):
    name = 'Noob Memer'
    level = 5
    role_id = 785676777585639464
    emoji = None

class level10(levels):
    name = 'Normie Memer'
    level = 10
    role_id = 785725155561308171
    emoji = None

class level15(levels):
    name = 'Dank Memer'
    level = 15
    role_id = 785676889736871946
    emoji = None

class level20(levels):
    name = 'Master Memer'
    level = 20
    role_id = 785725154373271594
    emoji = None

class level30(levels):
    name = 'OG Memer'
    level = 30
    role_id = 785676961904852992
    emoji = None

class level40(levels):
    name = 'Epic Memer'
    level = 40
    role_id = 785676992481329182
    emoji = None

class level50(levels):
    name = 'Legend Memer'
    level = 50
    role_id = 785726480092626945
    emoji = None

class level69(levels):
    name = 'Sexy Memer'
    level = 69
    role_id = 799844364976259082
    emoji = None

class level100(levels):
    name = 'God Memer'
    level = 100
    role_id = 810249129909420122
    emoji = None

### - - - - - Donations - - - - - ###
class donations:
    name = None
    amount = None
    role_id = None
    emoji = None

class mil5(donations):
    name = '5 Million Donator'
    amount = 5000000
    role_id = 787342154862166046
    emoji = '<a:5mil:855086694201557012>'

class mil10(donations):
    name = '10 Million Donator'
    amount = 10000000
    role_id = 787342156573704203
    emoji = '<a:10mil:855086693840584724>'

class mil25(donations):
    name = '25 Million Donator'
    amount = 25000000
    role_id = 799022090791419954
    emoji = '<:25mil:855086693472010272>'

class mil50(donations):
    name = '50 Million Donator'
    amount = 50000000
    role_id = 787868761528336427
    emoji = '<a:50mil:855086693974278154>'

class mil100(donations):
    name = '100 Million Donator'
    amount = 100000000
    role_id = 787868759720722493
    emoji = '<a:100mil:855086693932728350>'

class mil250(donations):
    name = '250 Million Donator'
    amount = 250000000
    role_id = 799844364389187616
    emoji = '<a:250mil:855086693445795861>'

class mil500(donations):
    name = '500 Million Donator'
    amount = 500000000
    role_id = 799022083778543696
    emoji = '<a:500mil:855086693710954496>'

class bil1(donations):
    name = '1 Billion Donator'
    amount = 1000000000
    role_id = 799844367551692827
    emoji = '<a:1bil:855086693619204096>'

class bil2_5(donations):
    name = '2.5 Billion Donator'
    amount = 2500000000
    role_id = 824615522934849607
    emoji = '<a:2_:855086693963399188>'

class bil5(donations):
    name = '5 Billion Donator'
    amount = 5000000000
    role_id = 786610853033541632
    emoji = '<a:5bil:855086693149704214>'

class topdonor(donations):
    name = 'Top Donator'
    amount = None
    role_id = 793189820151234620
    emoji = '<a:Crown:792881663398772746>'

### - - - - - Misc - - - - - ###
class misc:
    name = None
    role_id = None
    emoji = None

class staff(misc):
    name = 'Staff'
    role_id = 791516118120267806
    emoji = '<:staff:854882325556494356>'

class moneyDonor(misc):
    name = 'Money Donator'
    role_id = 815013978563543100
    emoji = None