from discord.ext import commands

from classes.Suggestions import Suggestion

class Recommendations(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.suggestion: Suggestion = Suggestion()

    @commands.command()
    async def sync(self, ctx: commands.Context):
        # if ctx.author.id == OWNER_USERID:
        #     await bot.tree.sync()
        #     await ctx.send('Command tree synced.')
        # else:
        #     await ctx.send('You must be the owner to use this command!')

        await self.bot.tree.sync()
        await ctx.send('Command tree synced.')

        print(self.bot.tree.get_commands())

    @commands.hybrid_command()
    async def recommend(self, ctx: commands.Context):
        rating_range = (1500, 1800)

        random_question_id = self.suggestion.suggest_problem(rating_range, "TODO")

        await ctx.send(random_question_id)