import discord
from discord.ext import commands

import pymongo.errors
from motor.motor_asyncio import AsyncIOMotorClient

class Afk(commands.Cog, name='AFK'):
    def __init__(self, bot):
        self.bot = bot
        self.motor_session = AsyncIOMotorClient('mongodb+srv://mainHost:TStB72SYJGmte1MC@brunis-utilities.okced.mongodb.net/afk?retryWrites=true&w=majority')
        self.db = self.motor_session.afk
    
    async def e(self, ctx):
        motor_session = AsyncIOMotorClient('mongodb+srv://mainHost:TStB72SYJGmte1MC@brunis-utilities.okced.mongodb.net/afk?retryWrites=true&w=majority')
        db = motor_session.afk

        guild_config = await db.guild_config.find_one({"_id": ctx.guild.id})
        roles = []

        for role in guild_config["accessable_roles"]:
            role = discord.utils.get(ctx.guild.roles, id=role)
            roles.append(role)

        for role in ctx.author.roles:
            if role in roles:
                return True

    # AFK
    @commands.group(name='afk', invoke_without_command=True)
    async def afk(self, ctx: commands.Context, *, reason = 'AFK'):
        if ctx.guild is None:
            return

        if not await self.e(ctx) and not ctx.author.guild_permissions.manage_guild:
            return await ctx.send('You do not have the required roles to run this command')

        guild_info = self.db[str(ctx.guild.id)]
        try:
            await guild_info.insert_one({"_id": ctx.author.id, "reason": reason, "name": ctx.author.display_name})
        except pymongo.errors.DuplicateKeyError:
            return await ctx.send('You are already afk')

        try:
            await ctx.author.edit(nick = '[AFK] ' + ctx.author.display_name)
        except:
            pass

        # as a precaution
        mentions = discord.AllowedMentions.none()
        mentions.users = True

        await ctx.send(f'{ctx.author.mention}: I have marked you afk for: {reason}', allowed_mentions = mentions)

    @afk.group(name='config', invoke_without_command=True)
    async def config(self, ctx):
        await ctx.send('Please send something to config')

    @config.group(name='access', invoke_without_command=True)
    async def access(self, ctx):
        await ctx.send('Please send something to config in access')

    @access.command(name='add')
    async def add(self, ctx, roles: commands.Greedy[discord.Role]):
        guild_config = await self.db.guild_config.find_one({"_id": ctx.guild.id})
        roles_ = []
        for role in roles:
            if role.id in guild_config["accessable_roles"]:
                continue
            roles_.append(role.name)
            await self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$push": {"accessable_roles": role.id}})

        await ctx.send(f'Added the following role(s) for using the afk command, however the manage server permission will bypass it: `{", ".join(roles_)}`')

    @access.command(name='remove')
    async def remove(self, ctx, roles: commands.Greedy[discord.Role]):
        guild_config = await self.db.guild_config.find_one({"_id": ctx.guild.id})
        roles_ = []
        for role in roles:
            if role.id in guild_config["accessable_roles"]:
                continue
            roles_.append(role.name)
            await self.db.guild_config.update_one({"_id": ctx.guild.id}, {"$pull": {"accessable_roles": role.id}})

        await ctx.send(f'Removed the following role(s) for using the afk command, however the manage server permission will bypass it: `{", ".join(roles_)}`')

    @commands.Cog.listener('on_message')
    async def unafk(self, message):
        if message.author.bot or 'afk' in message.content:
            return
        
        if message.guild is None:
            return

        guild_info = self.db[str(message.guild.id)]

        user_info = await guild_info.find_one({"_id": message.author.id})
        if user_info is None:
            return

        await guild_info.delete_one({"_id": message.author.id})
        try:
            await message.author.edit(nick = user_info["name"])
        except:
            pass
        await message.channel.send(f"Welcome back {message.author.mention}", delete_after = 5)

    @commands.Cog.listener('on_message')
    async def ping(self, message):
        if message.author.bot:
            return
        
        if message.guild is None:
            return

        if len(message.mentions) == 0:
            return

        guild_info = self.db[str(message.guild.id)]

        # this is so that many pings in a message would result in a single call to fetch instead of multiple calls
        bulk_mentions = True if len(message.mentions) >= 5 else False
        # in case multiple responses are needed
        responses = []

        if bulk_mentions:
            users_info = await guild_info.find()

            for mentioned in message.mentions:
                for ui in users_info:
                    if ui["_id"] == mentioned.id:
                        responses.append(f"{ui['name']} is currently AFK, {ui['reason']}")
        
        else:
            for mentioned in message.mentions:
                ui = await guild_info.find_one({"_id": mentioned.id})
                if ui is not None:
                    responses.append(f"{ui['name']} is currently AFK, {ui['reason']}")

        if responses == []:
            return

        await message.reply("\n".join(responses))

def setup(bot):
    bot.add_cog(Afk(bot))