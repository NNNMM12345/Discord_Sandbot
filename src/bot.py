import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, extensions):
        super().__init__(description="Hello friend",command_prefix='!', case_insensitive=True)

        # Load extension
        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print ('Failed to load extension {}\n{}'.format(extension, exc))


    async def on_ready(self):
        print('Logged in as {} ({})'.format(self.user.name, self.user.id))
