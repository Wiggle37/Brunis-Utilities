import asyncio
import discord

import aiosqlite

'''
Rewrite
'''
class donations:
    async def set(ctx, member, amount: int, category: str):
        async with aiosqlite.connect('dono.db') as dbase:
            await dbase.execute(f"INSERT INTO {ctx.guild.id} (user_id), {category}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {category} = ?;", [member.id, amount, amount])


categories = [
    'gaw',
    'heist',
    'event',
    'special'
]

async def get_amount(ctx, member: discord.Member):
    async with aiosqlite.connect('dono.db') as dbase:
        member = member or ctx.author

        cursor = await dbase.execute(f"SELECT total FROM donations WHERE user_id = '{member.id}'")
        amount = await cursor.fetchone()

    return amount[0]

'''
Normal
'''
class dono:
    # Set Any Dono Amount
    async def set(ctx, category, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in categories:
                return

            await dbase.execute(f"INSERT INTO donations (user_id, {category}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {category} = ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()
            return await get_amount(ctx, member)

    # Add Any Dono Amount
    async def add(ctx, category, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in categories:
                return
                
            await dbase.execute(f"INSERT INTO donations (user_id, {category}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {category} = {category} + ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()
            return await get_amount(ctx, member)

    # Remove Any Dono Amount
    async def remove(ctx, category, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in categories:
                return
                
            await dbase.execute(f"INSERT INTO donations (user_id, {category}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {category} = {category} - ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()
            return await get_amount(ctx, member)

    # Reset Any Dono Amount
    async def reset(ctx, category, member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in categories:
                return
                
            await dbase.execute(f"INSERT INTO donations (user_id, {category}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {category} = 0;", [member.id, 0])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()
            return await get_amount(ctx, member)

'''
Money
'''
class money:
    # Set Money Dono Amount
    async def set(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            await dbase.execute(f"INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()

    # Add Money Dono Amount
    async def add(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            await dbase.execute(f"INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money + ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()

    # Remove Money Dono Amount
    async def remove(member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            await dbase.execute(f"INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = money - ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()

    # Reset Money Dono Amount
    async def reset(member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            await dbase.execute(f"INSERT INTO donations (user_id, money) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET money = 0;", [member.id, 0])
            await dbase.execute(f"UPDATE donations SET total = gaw + heist + event + special WHERE user_id == {member.id}")

            await dbase.commit()