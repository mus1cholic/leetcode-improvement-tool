from discord.ext import commands
from typing import Optional

from classes.Suggestions import Suggestion, RecommendationEnum
from classes.Tags import TagsEnum

from bot.cogs.Views.TagMultiChoiceView import AdvancedRecommendView

from db.db import Database

"""
Contains commands relating to the recommendation system
"""

class Recommendations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()
        
        self.suggestion: Suggestion = Suggestion()

    @commands.hybrid_command()
    async def recommend(self, ctx: commands.Context,
                        difficulty: Optional[RecommendationEnum]):
        """
        Recommends a random leetcode question based on your profile

        Parameters
        -----------
        difficulty: RecommendationEnum, default: 2
            the difficulty of the problem
        """

        discord_user_id = ctx.message.author.id

        response = self.suggestion.suggest_problem(discord_user_id)

        response = f"{ctx.message.author.mention}, {response}"

        await ctx.send(response)

    @commands.hybrid_command()
    async def advancedrecommend(self, ctx: commands.Context):
        """
        Recommends a random leetcode question based on your profile with advanced configurations
        """

        discord_user_id = ctx.message.author.id

        view = AdvancedRecommendView(discord_user_id)

        message = await ctx.send(view=view, ephemeral=True)
        view.message = message