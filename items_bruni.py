from os import curdir
import sqlite3
import random
from typing import ClassVar

from discord import emoji

# dict of items for economy at the end

"""
    Base class for inheritance, a given category has to inherit this class before itself would be inherited to form actual items.
    
    Base attributes:
    name -- Display name for item
    description -- Display description for item

    image_url -- Image URL for embeds
    emoji -- Contains the custom emoji string
    db_name -- Name of item in database

    Inherited attributes:
    purchasable -- If purchasing is possible
    sellable -- If selling is possible
    price -- Amount required to purchase one item
    sell_price -- Amount given when selling one item

    table -- Table in database where item is located

    Functions:
    get_item_count -- Useful for inventory commands
    increase_item -- Handles logic for incrementing items
    decrease_item -- Handles logic for decrementing items
    purchase_items -- For buying items, handles incrementation of items and deduction of balance.
    sell_items -- For selling items, handles deduction items and incrementation of balance.

    If there need be, these functions can always be overridden, for custom implementation.

"""

class item:
    @classmethod
    def get_item_count(cls, user_id):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()

        cursor.execute(f"SELECT {cls.db_name} FROM {cls.table} WHERE user_id == ?", [user_id])
        item_count = cursor.fetchone()[0]
        dbase.close()
        return item_count

    @classmethod
    def increase_item(cls, user_id, count = 1):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} + ? WHERE user_id == ?", [count, user_id])

        dbase.commit()
        dbase.close()
    
    @classmethod
    def decrease_item(cls, user_id, count = 1):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {cls.table}  SET {cls.db_name} = {cls.db_name} - ? WHERE user_id == ?", [count, user_id])

        dbase.commit()
        dbase.close()

    @classmethod
    def purchase_items(cls, user_id, count = 1):
        if not cls.purchasable: # only purchase if an item is purchasable
            return

        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {currency.table} SET {currency.db_name} = {currency.db_name} - ? WHERE user_id == ?", [cls.price * count, user_id])

        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} + ? WHERE user_id == ?", [count, user_id])
        dbase.commit()
        dbase.close()
    
    @classmethod
    def sell_items(cls, user_id, count = 1):
        if not cls.sellable: # only purchase if an item is sellable
            return

        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {currency.table} SET {currency.db_name} = {currency.db_name} + ? WHERE user_id == ?", [cls.sell_price * count, user_id])

        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} - ? WHERE user_id == ?", [count, user_id])
        dbase.commit()
        dbase.close()


class currency:
    name = "Coins"
    table = "economy"
    db_name = "balance"
    emoji = "<:dankmerchant:852680899966271488>"

    @classmethod
    def add(cls, user_id, amount):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} + ? WHERE user_id == ?", [amount, user_id])
        dbase.commit()
        dbase.close()

    @classmethod
    def subtract(cls, user_id, amount):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} - ? WHERE user_id == ?", [amount, user_id])
        dbase.commit()
        dbase.close()

    @classmethod
    def get_amount(cls, user_id):
        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"SELECT {cls.db_name} FROM {cls.table} WHERE user_id == ?", [user_id])
        amount = cursor.fetchone()[0]
        dbase.close()
        return amount
        

class materials(item):
    table = "materials"
    purchasable = False
    price = None
    sellable = True


class wood(materials):
    name = "Wood"
    description = "Wood can be used for many things"
    image_url = "https://cdn.discordapp.com/emojis/852681061876236360.png?v=1"
    emoji = "<:bwood:852681061876236360>"
    db_name = "wood"
    sell_price = 50


class iron(materials):
    name = "Iron"
    description = "Used to make medal could probally sell for some good money"
    image_url = "https://cdn.discordapp.com/emojis/852681061318262825.png?v=1"
    emoji = "<:iron:852681061318262825>"
    db_name = "iron"
    sell_price = 100


class gold(materials):
    name = "Gold"
    description = "A pretty expensive mineral"
    image_url = "https://cdn.discordapp.com/emojis/852681061305679922.png?v=1"
    emoji = "<:gold:852681061305679922>"
    db_name = "gold"
    sell_price = 250


class diamond(materials):
    name = "Diamond"
    description = "A blue gem worth some money"
    image_url = "https://cdn.discordapp.com/emojis/852681061565726720.png?v=1"
    emoji = "<:diamond:852681061565726720>"
    db_name = "diamond"
    sell_price = 500


class emerald(materials):
    name = "Emerald"
    description = "A green gem worth a bit of money"
    image_url = "https://cdn.discordapp.com/emojis/852681061296898061.png?v=1"
    emoji = "<:emerald:852681061296898061>"
    db_name = "emerald"
    sell_price = 1000


class tools(item):
    table = "tools"
    purchasable = True
    sellable = False
    sell_price = None


class woodPick(tools):
    name = "Wooden Pickaxe"
    description = "The most basic pickaxe you have ever seen"
    image_url = "https://cdn.discordapp.com/emojis/852681061439504424.png?v=1" 
    emoji = "<:woodpick:852681061439504424>"
    db_name = "woodpick"
    price = 10000


class ironPick(tools):
    name = "Iron Pickaxe"
    description = "An entry level pickaxe"
    image_url = "https://cdn.discordapp.com/emojis/852681061702828032.png?v=1"
    emoji = "<:ironpick:852681061702828032>"
    db_name = "ironpick"
    price = 50000


class goldPick(tools):
    name = "Gold Pickaxe"
    description = "A very fast pickaxe"
    image_url = "https://cdn.discordapp.com/emojis/852681061585649714.png?v=1"
    emoji = "<:goldpick:852681061585649714>"
    db_name = "goldpick"
    price = 100000


class diamondPick(tools):
    name = "Diamond Pickaxe"
    description = "One of the best pickaxes"
    image_url = "https://cdn.discordapp.com/emojis/852681061351555174.png?v=1"
    emoji = "<:diamondpick:852681061351555174>"
    db_name = "diamondpick"
    price = 250000


class emeraldPick(tools):
    name = "Emerald Pickaxe"
    description = "The best of the pickaxes"
    image_url = "https://cdn.discordapp.com/emojis/852681061690507325.png?v=1"
    emoji = "<:emeraldpick:852681061690507325>"
    db_name = "emeraldpick"
    price = 500000


class gun(tools):
    name = "Gun"
    description = "You can use it to go hunting"
    image_url = "https://cdn.discordapp.com/emojis/852701370535903273.png?v=1" 
    emoji = "<:bgun:852701370535903273>"
    db_name = "gun"
    price = 100000
    

class fishingRod(tools):
    name = "Fishing Pole"
    description = "Have a nice peaceful time while fishing"
    image_url = "https://cdn.discordapp.com/emojis/852701358455914516.png?v=1"
    emoji = "<:fishingpole:852701358455914516>"
    db_name = "fishingpole"
    price = 75000

class axe(tools):
    name = 'Axe'
    description = 'An axe to chop some trees down'
    image_url = 'https://cdn.discordapp.com/emojis/851165794346729473.png?v=1'
    emoji = '<:axe:851165794346729473>'
    db_name = 'axe'
    price = 100000


class shovel(tools):
    name = 'Shovel'
    description = 'Go dig in the dirt and find some stuff maybe'
    image_url = 'https://cdn.discordapp.com/emojis/851172303873900564.png?v=1'
    emoji = '<:shovel:851172303873900564>'
    db_name = 'shovel'
    price = 100000


class multis(item):
    table = "multis"
    purchasable = False
    price = None
    sellable = False
    sell_price = None

    @classmethod
    def get_multi(cls, user_id):
        dbase = sqlite3.connect('economy.db')
        cursor = dbase.cursor()

        cursor.execute(f"SELECT doughnut FROM multis WHERE user_id == '{user_id}'")
        doughnut_amount = cursor.fetchone()[0]

        cursor.execute(f"SELECT token FROM multis WHERE user_id == '{user_id}'")
        token_amount = cursor.fetchone()[0]

        cursor.execute(f"SELECT brunisbackpack FROM multis WHERE user_id == '{user_id}'")
        backpack_amount = cursor.fetchone()[0]

        if doughnut_amount <= 0 and token_amount <= 0 and backpack_amount <= 0:
            return 0.01

        elif doughnut_amount > doughnut.cap or token_amount > butilCoin.cap or backpack_amount > brunisBackpack.cap:
            return (doughnut.cap * doughnut.multi) + (doughnut.cap * butilCoin.multi) + (doughnut.cap * brunisBackpack.multi)

        elif doughnut_amount < doughnut.cap or token_amount < butilCoin.cap and backpack_amount < brunisBackpack.cap:
            return (doughnut_amount * doughnut.multi) + (token_amount * butilCoin.multi) + (backpack_amount * brunisBackpack.multi)

        dbase.close()


class doughnut(multis):
    name = "Doughnut"
    description = "Gives an additional 5% multiplier when gambling"
    image_url = "https://cdn.discordapp.com/emojis/831895771442839552.png?v=1"
    emoji = "<:doughnut:831895771442839552>"
    db_name = "doughnut"
    multi = 0.05
    cap = 2


class brunisBackpack(multis):
    name = "Bruni's backpack"
    description = "Gives an additional 10% multiplier when gambling"
    image_url = "https://cdn.discordapp.com/emojis/834948572826828830.png?v=1"
    emoji = "<:brunisbackpack:834948572826828830>"
    db_name = "brunisbackpack"
    multi = 0.10
    cap = 1


class butilCoin(multis):
    name = "Bruni's Utilities Coin"
    description = 'Use these to buy some perks in the server'
    image_url = 'https://cdn.discordapp.com/emojis/851599382633250856.png?v=1'
    emoji = '<:brunisutils:851599382633250856>'
    db_name = 'token'
    multi = 0.05
    cap = 2


class misc(item):
    table = "items"
    purchasable = False
    price = None
    sellable = False
    sell_price = None


class apple(misc):
    name = "Apple"
    description = "An apple that does pretty much nothing for now"
    image_url = "https://cdn.discordapp.com/emojis/844760895951470612.png?v"
    emoji = '<:apple:844760895951470612>'
    db_name = "apple"
        

class duck(misc):
    name = "Duck"
    description = "QUACK"
    image_url = "https://cdn.discordapp.com/emojis/844761271378116639.png?v=1"
    emoji = "<:duck:844761271378116639>" 
    db_name = "duck"


class goose(misc):
    name = "Goose"
    description = None
    image_url = "https://cdn.discordapp.com/emojis/844762270549671956.png?v=1"
    emoji = "<:goose:844762270549671956>"
    db_name = "goose"


class chicken(misc):
    name = "Chicken"
    description = "UHHH *chicken noises*"
    image_url = "https://cdn.discordapp.com/emojis/844763374092943381.png?v=1"
    emoji = "<:chicken:844763374092943381>"
    db_name = "chicken"


class smallFish(misc):
    name = "Small fish"
    description = "A small fish you can get from fishing"
    image_url = "https://cdn.discordapp.com/emojis/852681061795495936.png?v=1"
    emoji = "<:smallfish:852681061795495936>"
    db_name = "smallfish"


class mediumFish(misc):
    name = "Medium Fish"
    description = "An average fish you can get from fishing"
    image_url = "https://cdn.discordapp.com/emojis/852681061481578527.png?v=1"
    emoji = "<:mediumfish:852681061481578527>"
    db_name = "mediumfish"


class largeFish(misc):
    name = "Large Fish"
    description = "The bigger of the fish that you can get from fishing"
    image_url = "https://cdn.discordapp.com/emojis/852681062253330452.png?v=1"
    emoji = "<:largefish:852681062253330452>"
    db_name = "largefish"


class iphone(misc):
    name = 'iPhone'
    description = 'Flex on the broke bitches\nSuggested by <@!801115086327644231>'
    image_url = 'https://cdn.discordapp.com/emojis/849373167913926728.png?v=1'
    emoji = '<:iphone:849373167913926728>'
    db_name = 'iphone'
    purchasable = True
    price = 20000000


class milkXmocha(misc):
    name = 'Milk and Mocha'
    description = 'A cute little collectors item\nSuggested by <@!732627627235606629>'
    image_url = 'https://cdn.discordapp.com/attachments/842372286265688096/850376992234930247/765171502671986709.png'
    emoji = '<:mm:851087059836862515>'
    db_name = 'milkMocha'
    purchasable = True
    price = 2000000


class rainbowblob(misc):
    name = 'Rainbow Blob'
    description = 'A rainbow blob that dances and nothing else'
    image_url = 'https://cdn.discordapp.com/emojis/829822719372951592.gif?v=1'
    emoji = '<a:blob:829822719372951592>'
    db_name = 'blob'
    purchasable = True
    price = 1000000000


class bananadance(misc):
    name = 'Dancing Banana'
    description = 'Just a dancing banana'
    image_url = 'https://cdn.discordapp.com/emojis/851094311466434560.gif?v=1'
    emoji = '<a:bananadance:851094311466434560>'
    db_name = 'bananadance'
    purchasable = True
    price = 500000000


class merchant(misc):
    name = 'Merchant Coin'
    description = 'This coin means everything, you are one of the richest people ever!'
    image_url = 'https://cdn.discordapp.com/emojis/810162519623991347.png?v=1'
    emoji = '<:dankmerchants:810162519623991347>'
    db_name = 'merchant'
    purchasable = True
    price = 10000000000


class squirt(misc):
    name = 'Squirt'
    description = 'Watcha ur eyes popin out <:thonk:797856990327734302>\nSuggested by <@!840223106345336882>'
    image_url = 'https://cdn.discordapp.com/emojis/800524219497840681.gif?v=1'
    emoji = '<a:squirt:800524219497840681>'
    db_name = 'squirt'
    purchasable = True
    price = 4000000


class badgeHeart(misc):
    name = 'Badge of Hearts'
    description = "If you have this badge you have discord addiction ~~don't deny it you know it's true~~\nSuggested by <@!833900274099290113>"
    image_url = 'https://cdn.discordapp.com/emojis/790751950689271819.png?v=1'
    emoji = '<:ty:790751950689271819>'
    db_name = 'hearts'
    purchasable = True
    price = 100000000


class dukesBadge(misc):
    name = "Duke's Badge"
    description = "The badge of Dukie\nSuggested by <@!716525960643739798>"
    image_url = 'https://cdn.discordapp.com/emojis/852514326156804137.gif?v=1'
    emoji = '<a:dukebadge:852514326156804137>'
    db_name = 'dukesbadge'


class snowflake(misc):
    name = 'Snowflake'
    description = 'Just a snowflake\nSuggested by <@!716525960643739798>'
    image_url = 'https://cdn.discordapp.com/emojis/852514325855207475.png?v=1'
    emoji = '<:bsnowflake:852514325855207475>'
    db_name = 'snowflake'
    purchasable = True
    price = 50000000


class uwuOwo(misc):
    name = 'UwU OwO Girl'
    description = '\nSuggested by <@!716525960643739798>'
    image_url = 'https://cdn.discordapp.com/emojis/852514326267035648.png?v=1'
    emoji = '<:uwuowo:852514326267035648>'
    db_name = 'uwuowo'
    purchasable = True
    price = 300000000


class darksbadge(misc):
    name = "Dark's Badge"
    description = "Well pretty easy to explain it's Dark's badge\nSuggested by <@!840223106345336882>"
    image_url = 'https://cdn.discordapp.com/emojis/852080742108233768.gif?v=1'
    emoji = '<a:DarkOP:852080742108233768>'
    db_name = 'darksbadge'
    purchasable = True
    price = 69000000


class boxes(item):
    table = "boxes"
    purchasable = True
    sellable = False
    sell_price = None
    
    @classmethod
    def usage(cls, user_id, count):
        # returns a response to send back

        response = "Box Contents:"
        if count > 1:
            response = f"Contents from {count} boxes:"

        dbase = sqlite3.connect("economy.db")
        cursor = dbase.cursor()
        cursor.execute(f"UPDATE {cls.table} SET {cls.db_name} = {cls.db_name} - ? WHERE user_id == ?", [count, user_id])
        for item, item_range in cls.possible_items.items():
            total_items = sum([random.randint(item_range[0], item_range[1]) for num in range(count)])
            cursor.execute(f"UPDATE {item.table} SET {item.db_name} = {item.db_name} + ? WHERE user_id == ?", [total_items, user_id])
            response += f"\n***{item.emoji} {item.name}:*** `{total_items}`"

        dbase.commit()
        dbase.close()
        return response


class woodenBox(boxes):
    name = "Wooden box"
    description = "A basic wooden box that could find you some loot"
    image_url = "https://cdn.discordapp.com/emojis/852681061254168616.png?v=1"
    emoji = "<:woodbox:852681061254168616>"
    db_name = "woodbox"
    price = 50000
    possible_items = {currency: [12500, 25000], apple: [0, 5]}
        

class ironBox(boxes):
    name = "Iron box"
    description = "A solid iron box probally has some good stuff in it"
    image_url = "https://cdn.discordapp.com/emojis/852681061308563516.png?v=1"
    emoji = "<:ironbox:852681061308563516>"
    db_name = "ironbox"
    price = 100000
    possible_items = {currency: [25000, 50000], apple: [0, 10], duck: [1, 5]}
    

class goldBox(boxes):
    name = "Gold box"
    description = "A solid gold box that must have good loot"
    image_url = "https://cdn.discordapp.com/emojis/852681061036195850.png?v=1"
    emoji = "<:goldbox:852681061036195850>"
    db_name = "goldbox"
    price = 250000
    possible_items = {currency: [50000, 100000], apple: [0, 15], duck: [1, 10]}
        

class diamondBox(boxes):
    name = "Diamond box"
    description = "A solid diamond box that is bound to have good loot"
    image_url = "https://cdn.discordapp.com/emojis/852681061032525865.png?v=1"
    emoji = "<:diamondbox:852681061032525865>"
    db_name = "diamondbox"
    price = 500000
    possible_items = {currency: [100000, 250000], apple: [1, 25], duck: [1, 25]}
        

class emeraldBox(boxes):
    name = "Emerald box"
    description = "The best box of them all that will have the best loot"
    image_url = "https://cdn.discordapp.com/emojis/852681060998971423.png?v=1"
    emoji = "<:emeraldbox:852681060998971423>"
    db_name = "emeraldbox"
    price = 1000000
    possible_items = {currency: [250000, 500000], apple: [1, 50], duck: [1, 10], doughnut: [0, 1]}


class wiggle(boxes):
    name = "Wiggle"
    description = "Really good loot can only be obtained on Wiggle's birthday"
    image_url = "https://cdn.discordapp.com/emojis/837799353111937066.gif?v=1"
    emoji = "<a:wiggle:840315403640635412>"
    db_name = "wiggle"
    price = None
    possible_items = {currency: [2500000,5000000], emeraldBox: [1,1]}
    table = "collectables"
    purchasable = False


class bruni(boxes):
    name = "Bruni"
    description = "Really good box that can only be obtained on bruni's birthday"
    image_url = "https://cdn.discordapp.com/attachments/784491141022220312/842934701470515240/bruni.gif"
    emoji = "<:brunisculpture:834947443434061864>"
    db_name = "bruni"
    price = None
    possible_items = {currency: [1000000, 15000000], emeraldBox: [1, 5], doughnut: [1, 3]}
    table = "collectables"
    purchasable = False


class babyBox(boxes):
    name = 'Baby Box'
    description = 'A box full of some stuff but in a baby box\nSuggested by <@!716525960643739798>'
    image_url = 'https://cdn.discordapp.com/emojis/852514326282895402.gif?v=1'
    emoji = '<a:babybox:852514325855207475>'
    db_name = 'babybox'
    price = None
    possible_items = {currency: [1000000, 5000000], iron: [2, 7], doughnut: [1, 2]}
    purchasable = False


items_classes = [
    woodenBox, ironBox, goldBox, diamondBox, emeraldBox, babyBox,
    wiggle, bruni,
    wood, iron, gold, diamond, emerald,
    woodPick, ironPick, goldPick, diamondPick, emeraldPick, gun, fishingRod, axe, shovel,
    doughnut, brunisBackpack, butilCoin,
    apple, duck, goose, chicken, smallFish, mediumFish, largeFish,
    iphone, milkXmocha, rainbowblob, bananadance, merchant, squirt, badgeHeart, uwuOwo, dukesBadge, snowflake, darksbadge
]

economy_items = {}
for i in items_classes:
    economy_items[i.name] = i

economy_items = dict(sorted(economy_items.items())) # sorts in alphabetical order