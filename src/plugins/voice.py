import discord
import youtube_dl
import asyncio
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Voice:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query: str=None):
        """Plays a file from the local filesystem"""
        if query == None:
            await ctx.send("Did you give me path to the file you want me to play?")
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
        else:
            try:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.send('Now playing: {}\nDefault volume is: 0.5'.format(query))
            except Exception as e:
                await ctx.send("I need a file from the local filesystem\n" + "Error Code: " + str(e))

    @commands.command()
    async def yt(self, ctx, *, url: str=None):
        """Plays from a url (almost anything youtube_dl supports)"""
        if url == None:
            await ctx.send("url?")
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
        else:
            try:
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.send('Now playing: {}\nDefault volume is: 0.5'.format(player.title))
            except Exception as e:
                await ctx.send("You did something wrong.\n" + "Error Code: " + str(e))
    @commands.command()
    async def stream(self, ctx, *, url: str=None):
        """Streams from a url (same as yt, but doesn't predownload)"""
        if url == None:
            await ctx.send("url?")
            try:
                await ctx.voice_client.disconnect()
            except:
                pass
        else:
            try:
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                await ctx.send('Now playing: {}\nDefault volume is: 0.5'.format(player.title))
            except Exception as e:
                await ctx.send("You did something wrong while trying to stream a video.\n" + "Error Code: " + str(e))
    @commands.command()
    async def volume(self, ctx, volume: str):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = float(volume)
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        try:
            await ctx.voice_client.disconnect()
        except Exception as e:
            await ctx.send("Is the bot connected to any voice channels?\n" + "Error Code: " + str(e))
    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Voice(bot))
