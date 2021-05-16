import sqlite3
import random

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
    emoji = "<:dankmerchants:829809749058650152>"

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
    image_url = "https://cdn.discordapp.com/emojis/835262637851541555.png?v=1"
    emoji = "<:mwood:835262637851541555>"
    db_name = "wood"
    sell_price = 50


class iron(materials):
    name = "Iron"
    description = "Used to make medal could probally sell for some money"
    image_url = "https://cdn.discordapp.com/emojis/834958446906441789.png?v=1"
    emoji = "<:iron:834958446906441789>"
    db_name = "iron"
    sell_price = 100


class gold(materials):
    name = "Gold"
    description = "A pretty expensive mineral"
    image_url = "https://cdn.discordapp.com/emojis/834958470955532338.png?v=1"
    emoji = "<:gold:834958470955532338>"
    db_name = "gold"
    sell_price = 250


class diamond(materials):
    name = "Diamond"
    description = "A blue gem worth some money"
    image_url = "https://cdn.discordapp.com/emojis/834958491315339294.png?v=1"
    emoji = "<:diamond:834958491315339294>"
    db_name = "diamond"
    sell_price = 500


class emerald(materials):
    name = "Emerald"
    description = "A green gem worth a bit of money"
    image_url = "https://cdn.discordapp.com/emojis/834958503369637941.png?v=1"
    emoji = "<:emerald:834958503369637941>"
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
    image_url = "https://cdn.discordapp.com/emojis/835505500035612772.png?v=1" 
    emoji = "<:woodpick:835505500035612772>"
    db_name = "woodpick"
    price = 10000


class ironPick(tools):
    name = "Iron Pickaxe"
    description = "An entry level pickaxe"
    image_url = "https://cdn.discordapp.com/emojis/835505509716197437.png?v=1"
    emoji = "<:ironpick:835505509716197437>"
    db_name = "ironpick"
    price = 50000


class goldPick(tools):
    name = "Gold Pickaxe"
    description = "A very fast pickaxe"
    image_url = "https://cdn.discordapp.com/emojis/835505519468740608.png?v=1"
    emoji = "<:goldpick:835505519468740608>"
    db_name = "goldpick"
    price = 100000


class diamondPick(tools):
    name = "Diamond Pickaxe"
    description = "One of the best pickaxes"
    image_url = "https://cdn.discordapp.com/emojis/835505528913264661.png?v=1"
    emoji = "<:diamondpick:835505528913264661>"
    db_name = "diamondpick"
    price = 250000


class emeraldPick(tools):
    name = "Emerald Pickaxe"
    description = "The best of the pickaxes"
    image_url = "https://cdn.discordapp.com/emojis/835505536744161330.png?v=1"
    emoji = "<:emeraldpick:835505536744161330>"
    db_name = "emeraldpick"
    price = 500000


class gun(tools):
    name = "Gun"
    description = "You can use it to go hunting"
    image_url = "https://cdn.discordapp.com/emojis/836051483224309790.png?v=1" 
    emoji = "<:gun:836051483224309790>"
    db_name = "gun"
    price = 100000
    

class fishingPole(tools):
    name = "Fishing Pole"
    description = "Have a nice peaceful time while fishing"
    image_url = "https://cdn.discordapp.com/emojis/836051493744148561.png?v=1"
    emoji = "<:fishingpole:836051493744148561>"
    db_name = "fishingpole"
    price = 75000


class multis(item):
    table = "multis"
    purchasable = False
    price = None
    sellable = False
    sell_price = None


class doughnut(multis):
    name = "Doughnut"
    description = "Gives an additional 5% multiplier when gambling"
    image_url = "https://cdn.discordapp.com/emojis/831895771442839552.png?v=1"
    emoji = "<:doughnut:831895771442839552>"
    db_name = "doughnut"


class brunisBackpack(multis):
    name = "Bruni's backpack"
    description = "Gives an additional 10% multiplier when gambling"
    image_url = "https://cdn.discordapp.com/emojis/834948572826828830.png?v=1"
    emoji = "<:brunisbackpack:834948572826828830>"
    db_name = "brunisbackpack"


class misc(item):
    table = "items"
    purchasable = False
    price = None
    sellable = False
    sell_price = None


class apple(misc):
    name = "Apple"
    description = None
    image_url = None
    emoji = None
    db_name = "apple"
        

class duck(misc):
    name = "Duck"
    description = None
    image_url = None
    emoji = None 
    db_name = "duck"


class goose(misc):
    name = "Goose"
    description = None
    image_url = None
    emoji = None
    db_name = "goose"


class chicken(misc):
    name = "Chicken"
    description = None
    image_url = None
    emoji = None
    db_name = "chicken"


class smallFish(misc):
    name = "Small fish"
    description = None
    image_url = None
    emoji = None
    db_name = "smallfish"


class mediumFish(misc):
    name = "Medium Fish"
    description = None
    image_url = None
    emoji = None
    db_name = "mediumfish"


class largeFish(misc):
    name = "Large Fish"
    description = None
    image_url = None
    emoji = None
    db_name = "largefish"


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
        for item, range in cls.possible_items.items():
            total_items = sum([random.randint(range[0], range[1]) for num in range(count)])
            cursor.execute(f"UPDATE {item.table} SET {item.db_name} = {item.db_name} + ? WHERE user_id == ?", [total_items, user_id])
            response += f"\n***{item.name}:*** `{total_items}`"

        dbase.commit()
        dbase.close()
        return response


class woodenBox(boxes):
    name = "Wooden box"
    description = "A basic wooden box that could find you some loot"
    image_url = "https://cdn.discordapp.com/emojis/830211928595890206.png?v=1"
    emoji = "<:woodbox:830211928595890206>"
    db_name = "woodenbox"
    price = 50000
    possible_items = {currency: [12500, 25000], apple: [0, 5]}
        

class ironBox(boxes):
    name = "Iron box"
    description = "A solid iron box probally has some good stuff in it"
    image_url = "https://cdn.discordapp.com/emojis/830197241934512188.png?v=1"
    emoji = "<:ironbox:830197241934512188>"
    db_name = "ironbox"
    price = 100000
    possible_items = {currency: [25000, 50000], apple: [0, 10], duck: [1, 5]}
    

class goldBox(boxes):
    name = "Gold box"
    description = "A solid gold box that must have good loot"
    image_url = "https://cdn.discordapp.com/emojis/830197220405805147.png?v=1"
    emoji = "<:goldbox:830197220405805147>"
    db_name = "goldbox"
    price = 250000
    possible_items = {currency: [50000, 100000], apple: [0, 15], duck: [1, 10]}
        

class diamondBox(boxes):
    name = "Diamond box"
    description = "A solid diamond box that is bound to have good loot"
    image_url = "https://cdn.discordapp.com/emojis/830197220007477259.png?v=1"
    emoji = "<:diamondbox:830197220007477259>"
    db_name = "diamondbox"
    price = 500000
    possible_items = {currency: [100000, 250000], apple: [1, 25], duck: [1, 25]}
        

class emeraldBox(boxes):
    name = "Emerald box"
    description = "The best box of them all that will have the best loot"
    image_url = "https://cdn.discordapp.com/emojis/830216613755486229.png?v=1"
    emoji = "<:emeraldbox:830216613755486229>"
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
    table = "collectibles"
    purchasable = False


class bruni(boxes):
    name = "Bruni"
    description = "Really good box that can only be optianed on bruni's birthday"
    image_url = "https://cdn.discordapp.com/attachments/784491141022220312/842934701470515240/bruni.gif"
    emoji = "<:brunisculpture:834947443434061864>"
    db_name = "bruni"
    price = None
    possible_items = {currency: [1000000, 15000000], emeraldBox: [1, 5], doughnut: [1, 3]}
    table = "collectables"
    purchasable = False


items_classes = [
    woodenBox, ironBox, goldBox, diamondBox, emeraldBox,
    wiggle, bruni,
    wood, iron, gold, diamond, emerald,
    woodPick, ironPick, goldPick, diamondPick, emeraldPick, gun,
    doughnut, brunisBackpack, 
    apple, duck, goose, chicken, smallFish, mediumFish, largeFish
]

# TODO: add in fishingpole in db lol

economy_items = {}
for i in items_classes:
    economy_items[i.name] = i


economy_items = dict(sorted(economy_items.items())) # sorts in alphabetical order
