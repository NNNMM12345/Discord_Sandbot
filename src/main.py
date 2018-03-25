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
import re
import math

########################################################################################################################
#FUNCTIONS

# Find will find the path to the api key from your home path
def find(name, path):
    start_time = time.time()
    print("Searching for an api key from: " + home + "...\nThis can take sometime")
    for root, dirs, files in os.walk(path):
        if name in files:
            print("Time spend searching was --- %s seconds ---" % (time.time() - start_time))
            return os.path.join(root, name)
        else:
            sys.exit("Could not find apiKey.text")


try:
    home = os.path.join(str(Path.home()), "Desktop")
    key_path = find("apiKey.txt", home)
    key_file = open(key_path, 'r')
except EnvironmentError:
    print("Couldn't open " + home + ", no such file")
else:
    with key_file:
        API_KEY = key_file.readline()

########################################################################################################################
# THE BOT

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Sandbot#1665", command_prefix="Sandbot", pm_help = False)

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
    print('You are running Sandbot v1.05')
    print('Created by The FuskerBrothers')
    return await client.change_presence(game=discord.Game(name='Sandboxing...'))


@client.event
async def on_message(message):
    if message.content.startswith('!messages'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!flip'):
        await client.send_message(message.channel, 'Flipping...')
        await client.send_message(message.channel, choice(['HEADS', 'TAILS']))

    elif message.content.startswith("!area"):
        try:
            if message.content[6:]:
                parameters = message.content[6:]
                split_lines = parameters.split(" ")

                num1 = int(split_lines[0])
                num2 = int(split_lines[1])
                num3 = int(split_lines[2])
                s = (num1 + num2 + num3) / 2
                area = s * (s - num1) * (s - num2) * (s - num3)
                area_final = math.sqrt(area)
                print(area_final)

                await client.send_message(message.channel, area_final)
            else:
                await client.send_message(message.channel, "I need numbers, Example !area [number] [number] [number]")
        except Exception as e:
            await client.send_message(message.channel,
                                      "I need numbers, Example !area [number] [number] [number]\nError Code: " + str(e))

    elif message.content.startswith("!roll"):
        await client.send_message(message.channel, "Rolling...")
        await client.send_message(message.channel, choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]))

    elif message.content.startswith('!wp'):
        if message.content[3:]:
            try:
                await client.send_message(message.channel, wikipedia.summary(str(message.content[3:]), sentences=1))
            except:
                await client.send_message(message.channel, "Can't find the thing you were looking for...")
        else:
            await client.send_message(message.channel, "I need input...")

    elif message.content.startswith('!help'):
        await client.send_message(message.channel, "COMMANDS YOU CAN USE\n!messages = Displays messages\n!flip = FLIPS a coin\n!wp = Searches from WIKIPEDIA\n!albums searches albums from an artist\n!math = just does math")

    elif message.content.startswith('!guess'):
        if message.content[6:]:
            try:
                answer = randint(1, 100)
                guess = message.content[6:]
                if guess == answer:
                    await client.send_message(message.channel, "YOU WON!!! Answer was:" + str(answer))
                elif guess < str(answer):
                    await client.send_message(message.channel, "You were too high  \nAnswer:" + str(answer))
                elif guess > str(answer):
                    await client.send_message(message.channel, "You were too low  \nAnswer:" + str(answer))
                else:
                    await client.send_message(message.channel, "You did something wrong")
            except Exception as e:
                await client.send_message(message.channel, "You definitely did something wrong:\n " + str(e))
        else:
            await client.send_message(message.channel, "Guess works like this !guess [number] it has to be in the range from 1-100")

    elif message.content.startswith('!albums'):
        if message.content[7:]:
            try:
                user = message.content[7:]
                albums = PyLyrics.getAlbums(str(user))
                await client.send_message(message.channel, albums)
            except Exception as e:
                await client.send_message(message.channel, "You did something wrong\n" + str(e))
        else:
             await client.send_message(message.channel, "Search for your artist like this\n !album [artist]")

    elif message.content.startswith('!lyrics'):
        try:
            if message.content[8:]:
                artist = re.split(r'[/]', str(message.content[8:]), re.I|re.M)
                print(artist)
                await client.send_message(message.channel, PyLyrics.getLyrics(str(artist[0]), str(artist[1])))
            else:
                await client.send_message(message.channel, "This works like this: !lyrics artist/songname the / is required else it doesnt work")
        except Exception as e:
            await client.send_message(message.channel, "This works like this: !lyrics artist/songname the / is required else it doesnt work\nError Code: " + str(e))

    elif message.content.startswith('!math'):
        try:
            await client.send_message(message.channel, eval(message.content[6:] ,{"__builtins__":None},{}))
        except Exception as e:
            await client.send_message(message.channel, message.content[6:] + "is not a valid expression")
            
# client runs api key securely implemented by johk3
client.run(str(API_KEY))

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
########################################################################################################################
#END
