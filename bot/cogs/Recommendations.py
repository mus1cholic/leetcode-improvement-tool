from discord.ext import commands

from typing import Optional

from classes.Suggestions import Suggestion, RecommendationEnum

"""
Contains commands relating to the recommendation system
"""

class Recommendations(commands.Cog):
    def __init__(self, bot: commands.Bot):
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

    @commands.hybrid_command()
    async def recommend(self, ctx: commands.Context,
                        difficulty: Optional[RecommendationEnum]):
        """
        Recommends a random leetcode question, based on your profile

        Parameters
        -----------
        difficulty: RecommendationEnum, default: 2
            the difficulty of the problem to recommend
        """

        # TODO: maybe have a simple recommend, and an advanced recommend

        rating_range = (1500, 1800)

        random_question_id = self.suggestion.suggest_problem(rating_range, "TODO")

        await ctx.send(random_question_id)