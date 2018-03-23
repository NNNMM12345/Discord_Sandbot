# -*- coding: utf-8 -*-
# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from random import randint
from random import choice
from PyLyrics import *
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import wikipedia
from pathlib import Path
import os
import time
########################################################################################################################
#FUNCTIONS

home = str(Path.home())

# Find will find the path to the api key from your home path


def find(name, path):
    start_time = time.time()
    print("Searching for an api key from: " + home + "...\nThis can take sometime")
    for root, dirs, files in os.walk(path):
        if name in files:
            print("Time spend searching was --- %s seconds ---" % (time.time() - start_time))
            return os.path.join(root, name)


with open(find("apiKey.txt", home), 'r') as f:
    # Api list is the api in a list format
    apilist = f.readlines()
    # .join will convert the list to a string
    print("Api key: " + ''.join(apilist))
    api_key = ''.join(apilist)

########################################################################################################################
# THE BOT

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Sandbot#1665", command_prefix="Sandbot", pm_help = False)

########################################################################################################################
# EVENTS

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Usemessage.content[3:] this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Support Discord Server: https://discord.gg/qSpwrdq')
    print('Github Link: https://github.com/NNNMM12345/Discord_Sandbot')
    print('--------')
    print('You are running Sandbot v1.0')
    print('Created by The FuskerBrothers')
    return await client.change_presence(game=discord.Game(name='Sandboxing...'))


# @client.event
# async def on_message(message):
#     if message.content.startswith('!messages'):
#         counter = 0
#         tmp = await client.send_message(message.channel, 'Calculating messages...')
#         async for log in client.logs_from(message.channel, limit=100):
#             if log.author == message.author:
#                 counter += 1

#         await client.edit_message(tmp, 'You have {} messages.'.format(counter))

#     elif message.content.startswith('!flip'):
#         await client.send_message(message.channel, 'Flipping...')
#         await client.send_message(message.channel, choice(['HEADS', 'TAILS']))

#     elif message.content.startswith('!wp'):
#         if message.content[3:]:
#             try:
#                 await client.send_message(message.channel, wikipedia.summary(str(message.content[3:]), sentences=1))
#             except:
#                 await client.send_message(message.channel, "Can't find the thing you were looking for...")
#         else:
#             await client.send_message(message.channel, "I need input...")

#     elif message.content.startswith('!help'):
#         await client.send_message(message.channel, "COMMANDS YOU CAN USE\n!messages = Displays messages\n!flip = FLIPS a coin\n!wp = Searches from WIKIPEDIA\n!albums searches albums from an artist")

#     elif message.content.startswith('!guess'):
#         if message.content[6:]:
#             try:
#                 answer = randint(1, 100)
#                 guess = message.content[6:]
#                 if guess == answer:
#                     await client.send_message(message.channel, "YOU WON!!! Answer was:" + str(answer))
#                 elif guess < str(answer):
#                     await client.send_message(message.channel, "You were too high  \nAnswer:" + str(answer))
#                 elif guess > str(answer):
#                     await client.send_message(message.channel, "You were too low  \nAnswer:" + str(answer))
#                 else:
#                     await client.send_message(message.channel, "You did something wrong")
#             except Exception as e:
#                 await client.send_message(message.channel, "You definitely did something wrong:\n " + str(e))
#         else:
#             await client.send_message(message.channel, "Guess works like this !guess [number] it has to be in the range from 1-100")

#     elif message.content.startswith('!albums'):
#         if message.content[7:]:
#             try:
#                 user = message.content[7:]
#                 albums = PyLyrics.getAlbums(str(user))
#                 await client.send_message(message.channel, albums)
#             except Exception as e:
#                 await client.send_message(message.channel, "You did something wrong\n" + str(e))
#         else:
#              await client.send_message(message.channel, "Search for your artist like this\n !album [artist]")

# END EVENTS
########################################################################################################################
# COMMANDS

@client.command(name = "messages",
                description = "Prints the number of past messages from the requester.",
                pass_context = True)
async def messages(context):
    message = context.message
    count = 0
    await client.say("Calculating messages...")
    async for log in client.logs_from(message.channel, limit = 100):
        if log.author == message.author:
            count += 1
    
    await client.say("You have {} messages.".format(count))

@client.command(name = "flip",
                description = "Flips a coin.")
async def flip():
    await client.say("Flipping...")
    await client.say(choice(["HEADS", "TAILS"]))

@client.command(name = "wp",
                description = "Prints the first sentence of the Wikipedia article with the given title.",
                pass_context = True)
async def wp(context):
    message = context.message
    text = message.content
    split_lines = text.split(" ")
    
    if not split_lines[1:]:
        await client.say("You must specify the article to find.")
        return
    
    try:
        query = " ".join(split_lines[1:])
        summary = wikipedia.summary(query, sentences = 1)
        await client.say(summary)
    except:
        await client.say("The page could not be retrieved successfully.")

# @client.command(name = "help",
#                 description = "Outputs the list of possible commands.")
# async def help():
#     await client.say("COMMANDS YOU CAN USE\n!messages = Displays messages\n!flip = FLIPS a coin\n!wp = Searches from WIKIPEDIA\n!albums searches albums from an artist")

@client.command(name = "guess",
                description = "Plays a game where the user guesses a number between 1 and 100 and tells them if they got it right.",
                pass_context = True)
async def guess(context):
    message = context.message
    split_lines = message.content.split(" ")

    if not split_lines[1]:
        await client.say("Guess works like this: !guess [number] where [number] is between 1 and 100.")
        return

    answer = randint(1, 100)
    guess = int(split_lines[1])

    if (guess < 1) or (guess > 100):
        await client.say("The number must be between 1 and 100.")
        return
    
    if (guess == answer):
        await client.say("You got it right!")
    elif (guess < answer):
        await client.say("You were too low.")
    elif (guess > answer):
        await client.say("You were too high.")
    else:
        await client.say("Something went wrong.")

@client.command(name = "albums",
                description = "Gets information on the albums of the given artist",
                pass_context = True)
async def albums(context):
    message = context.message
    split_lines = message.content.split(" ")

    if not split_lines[1:]:
        client.say("Search for your artist like this\n !album [artist]")
        return
    
    artist_name = " ".join(split_lines[1:])
    albums = PyLyrics.getAlbums(artist_name)
    await client.say(albums)

# END COMMANDS
########################################################################################################################

# client runs api key securely implemented by johk3
client.run(api_key)

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
########################################################################################################################
#END
