import discord
from discord.ext import commands

class Bot(commands.Bot):
    
    def __init__(self, plugins):
        super().__init__(command_prefix='!', case_insensitive=True)
        # Load extension
        for plugin in plugins:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print ('Failed to load extension {}\n{}'.format(extension, exc))


    async def on_ready(self):
        print('Logged in as {} ({})'.format(self.user.name, self.user.id))
