import discord

import aiosqlite

class giveaway:
    # Set Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Add Amount
    @staticmethod
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw + ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Remove Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = gaw - ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Reset Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET gaw = ?;", [member.id, 0, 0])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

class heist:
    # Set Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Add Amount
    @staticmethod
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, gaw) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist + ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Remove Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = heist - ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Reset Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, heist) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET heist = ?;", [member.id, 0, 0])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

class event:
    # Set Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Add Amount
    @staticmethod
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event + ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Remove Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = event - ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Reset Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, event) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET event = ?;", [member.id, 0, 0])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

class special:
    # Set Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Add Amount
    @staticmethod
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special + ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Remove Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = special - ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Reset Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, special) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET special = ?;", [member.id, 0, 0])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

class money:
    # Set Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Add Amount
    @staticmethod
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Remove Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money - ?;", [member.id, amount, amount])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()

    # Reset Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            dbase.execute("INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = ?;", [member.id, 0, 0])
            dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            dbase.commit()