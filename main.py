###Imports###
import discord
from discord import Activity, ActivityType, Color, Embed, User
from discord.ext import commands
from discord.ext.commands import Bot

import asyncio

import os
from dotenv import load_dotenv

###Bot###
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    command_prefix=['b!', 'B!'],
    intents=intents,
    case_insensitive=True,
    )
client.remove_command('help')

###On Ready###
@client.event
async def on_ready():
    print(f'Bot is now online!\n--------------------\nUser: {client.user}\nID: {client.user.id}')

###Cog Loader###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded **{extension}**')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded **{extension}**')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded **{extension}**')

async def status():
    await client.wait_until_ready()
    while True:
        memberCount = sum([guild.member_count for guild in client.guilds])
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over {memberCount} people'))

        await asyncio.sleep(30)

client.loop.create_task(status())

###Run Bot###
load_dotenv()
Bot_Token = os.getenv('BOT_TOKEN')
client.run(Bot_Token)

# This script will walk through all sub-directories in the current directory
# and pull the most recent updates

import argparse

# Parse cmd line args
descriptionText = 'This script will walk through all sub-directories, fetch all tags, and pull.'
parser = argparse.ArgumentParser(descriptionText)
parser.add_argument("-t", "--tag", help="Checkout this branch or tag for each repo")
parser.add_argument("-d", "--directory", help="The direcotry that holds all the repos you want to update. Default is current dir.")
parser.add_argument("-b", "--branch", help="After pulling and checking out, create a new branch of this name for each repo")

args = parser.parse_args()

# Store the starting direcotry
rootDir = os.getcwd()

# If we used an arg for the direcotry, then use that instead of the current 
if args.directory:
    rootDir = args.directory

print("\n----- Auto Pull config --------")
print("Directory: " + rootDir)

if args.tag:
    print("Checkout: ", args.tag)
else:
    print("Checkout: NONE")

if args.branch:
    print("New branch: " + args.branch)
else:
    print("New branch: NONE")
print("-------------------------------\n")

for currentDir in filter(os.path.isdir, os.listdir(rootDir)):
    
    print("\n------\nUpdating: " + currentDir)
    # Change directories
    os.chdir(currentDir)

    # Get the most recent tags and pull latest
    os.system("git status")
    os.system("git checkout --theirs .")

    # Update all tags and check one out if specified
    os.system("git fetch --all --tags --prune -q")  
    os.system("git pull --quiet")

    if args.tag:
        os.system("git checkout " + args.tag)

    
    # Create a new branch if specified
    if args.branch:
        os.system("git checkout -b " + args.branch)

    # Go back to the original directory
    os.chdir(rootDir)

print("-------- Update complete! --------")