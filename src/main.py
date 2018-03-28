from bot import Bot
import settings.config

extensions = ['plugins.general', 'plugins.voice']

def main():
    bot = Bot(extensions) 
    bot.run(settings.config.DISCORD_TOKEN)

if __name__ == '__main__':
    main()
