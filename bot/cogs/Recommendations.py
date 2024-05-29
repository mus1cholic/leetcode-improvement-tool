from discord.ext import commands

from typing import Optional

from classes.Suggestions import Suggestion, RecommendationEnum
from classes.Tags import TagsEnum

from db.db import Database

"""
Contains commands relating to the recommendation system
"""

class Recommendations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()
        
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
        """

        discord_user_id = ctx.message.author.id

        response = self.suggestion.suggest_problem(discord_user_id)

        response = f"{ctx.message.author.mention}, {response}"

        await ctx.send(response)

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

        tags: TagsEnum, default: Overall
            a multiple-choice for all the tags to include
        """

        print(tags)

        await ctx.send("hi!")