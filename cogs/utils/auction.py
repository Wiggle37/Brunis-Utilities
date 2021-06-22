from discord.ext import commands
import discord
import sys
import traceback
import asyncio

from discord.ext.commands.errors import MissingRequiredArgument


class Auction(commands.Cog, name='auction', description='Host some auctions for the server'):
    def __init__(self, client):
        self.client = client
        self.auctioner_role = client.get_guild(784491141022220309).get_role(800496416740605993)
        self.emoji = "\U0001f3e6"
        self.auction_message_id = None
        self.auction_in_progress = False
        self.started_bidding = False
        self.auction_amount = 1
        self.highest_bidder = None
    
    def reset(self):
        self.auction_message_id = None
        self.auction_in_progress = False
        self.started_bidding = False
        self.auction_amount = 1
        self.highest_bidder = None

    def beautify_number(self, num):
        return '{:,}'.format(num)

    def is_valid_int(self, amount):
        try:
            float(amount.replace("m","").replace("k",""))
            return int(eval(amount.replace("k","e3").replace("m", "e6")))
            
        except ValueError:
            return False
        
    async def add_auction_role(self, user):
        await user.add_roles(self.auctioner_role)

    async def five_reactions(self, message_id, emoji):
        def check(reaction, user):
            return str(reaction.emoji) == emoji and reaction.message.id == message_id
        
        reaction, user = await self.client.wait_for("reaction_add", check=check)
        if reaction.count < 4:
            return await self.five_reactions(message_id, emoji)


    async def give_auction_role(self, message_id, emoji):
        def check(reaction, user):
            return str(reaction.emoji) == emoji and reaction.message.id == message_id

        while self.auction_in_progress:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=check, timeout = 30)
                # if the auction halts while waiting and someone reacts to the message

                if self.auction_in_progress:
                    await self.add_auction_role(user)

            except asyncio.TimeoutError:
                pass
    
    async def call_counts(self, ctx):
        while self.auction_in_progress:
            if not self.started_bidding:
                await asyncio.sleep(3)
                continue
            
            current_bid = self.auction_amount

            await asyncio.sleep(15)
            if current_bid != self.auction_amount:
                continue
            await ctx.send(f"Calling once for ⏣**{self.beautify_number(current_bid)}**")


            await asyncio.sleep(10)
            if current_bid != self.auction_amount:
                continue
            await ctx.send(f"Calling twice for ⏣**{self.beautify_number(current_bid)}**")

            await asyncio.sleep(5)
            if current_bid != self.auction_amount:
                continue

            return await self.auctionend(ctx)


    @commands.command(name='auctionstart', description='Start an auction to auction of an item for some money', aliases=["as"])
    @commands.has_any_role(784492058756251669, 784527745539375164, 802645887063031818, 785202756641619999, 788738308879941633, 840738395001323563) #Admin, Mod, Auctioneer, Bruni, client Dev
    async def auctionstart(self, ctx, starting_bid, *, item):
        starting_bid = self.is_valid_int(starting_bid)
        if starting_bid == False:
            return await ctx.reply("That's not a valid amount")

        if self.auction_in_progress:
            return await ctx.send("An auction is already being held!")
        
        self.auction_amount = starting_bid
        self.auction_in_progress = True

        auction_embed = discord.Embed(
            title = f"An auction is starting!\nReact with {self.emoji} to get started! ",
            colour = 0x5865f2
        )

        auction_embed.add_field(
            name = "Roles will be given out when 3 people have reacted",
            value = f"Bidding for: {item}\nStarting bid is at ⏣**{self.beautify_number(self.auction_amount)}**\nMay the best bidder win!",
            inline = False
        )

        auction_embed.add_field(
            name = "Timings for calls",
            value = "First call will be at 15 seconds after last bid, second call at 10 seconds and final call at 5 seconds",
            inline = False
        )
        
        auction_message = await ctx.send(embed = auction_embed)
        await auction_message.add_reaction(self.emoji)
        self.auction_message_id = auction_message.id

        try:
            await asyncio.wait_for(self.five_reactions(auction_message.id, self.emoji), 300)
        except asyncio.TimeoutError:
            self.reset()
            return await ctx.send("Well looks like nobody wants auctions")

        # gets the updated reactions
        auction_message = await ctx.fetch_message(self.auction_message_id)

        # adds all the roles to people
        for reaction in auction_message.reactions:
            if str(reaction.emoji) == self.emoji:
                for user in await reaction.users().flatten():
                    await self.add_auction_role(user)
        
        await ctx.send("Let the bidding begin! `b!bid <amount>` to bid.\nPsst, you can use `m` and `k` to denote millions and thousands")
        
        await asyncio.gather(
            self.give_auction_role(auction_message.id, self.emoji),
            self.call_counts(ctx)
        )

    @auctionstart.error
    async def as_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            return
        
        if isinstance(error, MissingRequiredArgument):
            return await ctx.reply("It's `b!as <starting bid> <item(s)>`")
        
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    @commands.command(name='bid', description='Add to the bid of the current auction', aliases = ["a"])
    async def auction(self, ctx, bid):
        if not self.auction_in_progress:
            return
        
        if ctx.channel.id != 789227950636793887:
            return
        
        bid = self.is_valid_int(bid)
        if bid == False:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention} That's not a valid number")
        
        if bid < self.auction_amount and not self.started_bidding:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}The minimum bid is ⏣**{self.beautify_number(self.auction_amount)}**")

        if bid <= self.auction_amount and self.started_bidding:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention} Someone else has bid a higher price")
        
        self.auction_amount = bid
        self.highest_bidder = ctx.author
        if not self.started_bidding: self.started_bidding = True

        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} bid ⏣**{self.beautify_number(bid)}**")
    
    @auction.error
    async def auction_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply("You need to key in a bid")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    async def auctionend(self, ctx):
        auction_message = await ctx.fetch_message(self.auction_message_id)
        
        # removes all the roles from people
        for reaction in auction_message.reactions:
            if str(reaction.emoji) == self.emoji:
                for user in await reaction.users().flatten():
                    await user.remove_roles(self.auctioner_role)
        
        auction_end_embed = discord.Embed(
            title = "Auction ended!",
            colour = 0x5865f2
        )

        auction_end_embed.add_field(
            name = "Sold to:",
            value = f"{self.highest_bidder.mention}, With a bid of ⏣**{self.beautify_number(self.auction_amount)}**",
            inline = False
        )

        auction_end_embed.add_field(
            name = "Want to auction something of your own?",
            value = "Head to <#790923047837761556> and put your item + price there and a staff member will get to you.",
            inline = False
        )

        self.reset()
        await ctx.send(embed = auction_end_embed)

def setup(client):
    client.add_cog(Auction(client))