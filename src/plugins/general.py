import discord
from discord.ext import commands


import random
import wikipedia
from PyLyrics import *

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        "Flip a coin"
        await ctx.send('Flipping...')
        await ctx.send(random.choice(['HEADS', 'TAILS']))

    @commands.command()
    async def math(self, ctx, *, param: str = None):
        "Solves basic mathematical operations"
        if param == None:
            await ctx.send('Start easy... 1 + 1?')
        else:
            try:
                await ctx.send(eval(param, {"__builtins__":None},{}))
            except Exception as e:
                await ctx.send(param + "is not a valid expression")

    @commands.command()
    async def roll(self, ctx):
        "Rolls a dice from 1 to 10"
        await ctx.send('Rolling...')
        await ctx.send(random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']))

    @commands.command(aliases=['wp'])
    async def wikipedia(self, ctx, *, param: str = None):
        "Searches your thing on wikipedia"
        try: 
            if param == None:
                await ctx.send("You don't know what to search ? What about turtle?")
                summary = wikipedia.summary("turtle", sentences=2)
            else:
                summary = wikipedia.summary(param, sentences=1)
            await ctx.send(summary)
        except Exception as e:
            await ctx.send("Bip bip, something went wrong. What are you looking for again?")

    @commands.command()
    async def guess(self, ctx, param: str=None):
        "!guess [number] it has to be in the range from 1-100"
        if param == None:
            await ctx.send("Guess works like this !guess [number] it has to be in the range from 1-100")
        else:
            try:
                guess = int(param)
                answer = random.randint(1, 100)
                if guess == int(answer):
                    await ctx.send("YOU WON!!! Answer was:" + str(answer))
                elif guess < int(answer):
                    await ctx.send("You were too low  \nAnswer:" + str(answer))
                elif guess > int(answer):
                    await ctx.send("You were too high  \nAnswer:" + str(answer))
                else:
                    await ctx.send("You did something wrong")
            except Exception as e:
                await ctx.send("You definitely did something wrong:\n" + str(e))

    @commands.command()
    async def lyrics(self, ctx, *, param: str = None):
        "Search your lyrics like this !lyrics artist/song"
        try:
            if param == None:
                await ctx.send("This works like this: !lyrics artist/songname the / is required else it doesnt work")
            else:
                artist, song = param.split('/')
                await ctx.send(PyLyrics.getLyrics(str(artist), str(song)))
        except Exception as e:
            await ctx.send("This works like this: !lyrics artist/songname the / is required else it doesnt work\nError Code: " + str(e))

    @commands.command()
    async def albums(self, ctx, *, param: str):
        "Searches for artist's all albums"
        if param == None:
            await ctx.send("Search for your artist like this\n !album [artist]")
        else:
            try:
                albums = PyLyrics.getAlbums(param)
                await ctx.send(albums)
            except Exception as e:
                await ctx.send("You did something wrong\n" + str(e))


def setup(bot):
    bot.add_cog(General(bot))
