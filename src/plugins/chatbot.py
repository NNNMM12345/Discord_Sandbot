import discord
from discord.ext import commands
from chatterbot import ChatBot

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")


class TheChatBot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx,*, something: str=None):
        """Just !ask something from the bot"""
        if something == None:
            await ctx.send("You need to give me some input...")
        else:
            try:
                await ctx.send(str(chatbot.get_response(something)))
            except Exception as e:
                await ctx.send("I think the chatbot might be down :(\nError Code: " + str(e))


def setup(bot):
    bot.add_cog(TheChatBot(bot))