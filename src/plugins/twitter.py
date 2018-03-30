import tweepy
import discord
from discord.ext import commands

auth = tweepy.OAuthHandler("v1YMI0FMRDOoOlTqmifKhy2hC", "PJKTdJUmk8cGtgPUuDGNeSxxiBrPrfP4e73OtG7yeZbVDj17zt")
auth.set_access_token("903928713343102976-AOv7IGe2SKtg54UO0DPimBF8qhUMDmh", "VnjIHwJrTYsOADxcnZBeb6JWrYwPfK5Lfc0UcTrKosS1f")
api = tweepy.API(auth)


class Twitter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tweet(self, ctx, subject: str=None):
        """!tweet [something] searches for 5 of that something"""
        if subject == None:
            await ctx.send("Give me some topic to search for")
        else:
            try:
                public_tweets = api.search(subject)
                count = 0
                for tweet in public_tweets:
                    count += 1
                    await ctx.send(tweet.text)
                    if count >= 5:
                        break
            except Exception as e:
                await ctx.send("Sorry something went wrong\nError Code: " + str(e))

    @commands.command()
    async def users(self, ctx, something: str=None):
        """Searches for 20 users that are linked to your input"""
        if something == None:
            await ctx.send("Can you give me something to search?")
        else:
            try:
                user = api.get_user(something)
                listsomething = []
                count = 0
                for friend in user.friends():
                    listsomething.append(friend.screen_name)
                    count += 1
                    if count >= 20:
                        await ctx.send("\n".join(listsomething))
            except Exception as e:
                await ctx.send("Sorry something went wrong\nError code: " + str(e))

def setup(bot):
    bot.add_cog(Twitter(bot))
