from discord.ext import commands

from typing import Optional

from classes.Suggestions import Suggestion, RecommendationEnum
from classes.Tags import TagsEnum

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

        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send('Command tree synced.')

    @commands.hybrid_command()
    async def recommend(self, ctx: commands.Context):
        """
        Recommends a random leetcode question based on your profile

        Parameters
        -----------
        difficulty: RecommendationEnum, default: 2
            the difficulty of the problem to recommend
        """

        # TODO: maybe have a simple recommend, and an advanced recommend

        rating_range = (1500, 1800)

        random_question_id = self.suggestion.suggest_problem(rating_range, "TODO")

        await ctx.send(random_question_id)

    @commands.hybrid_command()
    async def advancedrecommend(self, ctx: commands.Context,
                                difficulty: Optional[RecommendationEnum],
                                tags: Optional[TagsEnum]):
        """
        Recommends a random leetcode question based on your profile with advanced configurations

        Parameters
        -----------
        difficulty: RecommendationEnum, default: 2
            the difficulty of the problem to recommend

        tags: TagsEnum, optional
            a multiple-choice for all the tags to include
        """

        print(tags)

        await ctx.send("hi!")