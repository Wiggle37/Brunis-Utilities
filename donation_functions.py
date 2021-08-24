import discord
from discord.ext import commands

import aiosqlite

class donations:
    # Get Ammounts
    async def get_amounts(ctx, member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            member = member or ctx.author

            cursor = await dbase.execute(f"SELECT giveaway, heist, event, special, money, total FROM '{ctx.guild.id}' WHERE user_id = '{member.id}'")
            amount = await cursor.fetchone()

        return amount

    # Get Total Ammount
    async def get_amount(ctx, member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            member = member or ctx.author

            cursor = await dbase.execute(f"SELECT giveaway FROM '{ctx.guild.id}' WHERE user_id = '{member.id}'")
            amount = await cursor.fetchone()

        return amount[0]

    categories = {
        0: 'giveaway',
        1: 'heist',
        2: 'event',
        3: 'special',
        4: 'money'
    }

    # Set Any Dono Amount
    async def set(ctx, category: int, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in donations.categories:
                return

            await dbase.execute(f"INSERT INTO '{ctx.guild.id}' (user_id, {donations.categories[category]}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {donations.categories[category]} = ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE '{ctx.guild.id}' SET total = giveaway + heist + event + special WHERE user_id == '{member.id}'")
            await dbase.commit()

    # Add Any Dono Amount
    async def add(ctx, category: int, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in donations.categories:
                return
                
            await dbase.execute(f"INSERT INTO '{ctx.guild.id}' (user_id, {donations.categories[category]}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {donations.categories[category]} = {donations.categories[category]} + ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE '{ctx.guild.id}' SET total = giveaway + heist + event + special WHERE user_id == '{member.id}'")
            await dbase.commit()

    # Remove Any Dono Amount
    async def remove(ctx, category: int, member: discord.Member, amount: int):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in donations.categories:
                return
                
            await dbase.execute(f"INSERT INTO '{ctx.guild.id}' (user_id, {donations.categories[category]}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {donations.categories[category]} = {donations.categories[category]} - ?;", [member.id, amount, amount])
            await dbase.execute(f"UPDATE '{ctx.guild.id}' SET total = giveaway + heist + event + special WHERE user_id == '{member.id}'")
            await dbase.commit()

    # Reset Any Dono Amount
    async def reset(ctx, category: int, member: discord.Member):
        async with aiosqlite.connect('dono.db') as dbase:
            if category not in donations.categories:
                return
                
            await dbase.execute(f"INSERT INTO '{ctx.guild.id}' (user_id, {donations.categories[category]}) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET {donations.categories[category]} = 0;", [member.id, 0])
            await dbase.execute(f"UPDATE '{ctx.guild.id}' SET total = giveaway + heist + event + special WHERE user_id == '{member.id}'")
            await dbase.commit()
