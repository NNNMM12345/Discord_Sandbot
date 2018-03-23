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

API_KEY_NAME = "apiKey.txt"

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
    print('You are running Sandbot v1.0')
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

    elif message.content.startswith('!wp'):
        if message.content[3:]:
            try:
                await client.send_message(message.channel, wikipedia.summary(str(message.content[3:]), sentences=1))
            except:
                await client.send_message(message.channel, "Can't find the thing you were looking for...")
        else:
            await client.send_message(message.channel, "I need input...")

    elif message.content.startswith('!help'):
        await client.send_message(message.channel, "COMMANDS YOU CAN USE\n!messages = Displays messages\n!flip = FLIPS a coin\n!wp = Searches from WIKIPEDIA\n!albums searches albums from an artist")

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

# This function reads the API key from the file with the given name.
def get_api_key(file_name):
    file = open(file_name, "r")
    return file.read()

# Passes in the API key to client.run() to initialize the bot.
api_key = get_api_key(API_KEY_NAME)
client.run(api_key)

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.