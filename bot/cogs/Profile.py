import discord

from typing import Optional

from discord.ext import commands

from classes.Builders import Builder
from classes.Tags import TagsEnum

from db.db import Database

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()

    @commands.hybrid_command()
    async def profile(self, ctx: commands.Context):
        """
        View your Leetcode profile and various statistics
        """
        
        discord_user_id = ctx.message.author.id

        user = self.db.find_user(discord_user_id)

        if not user:
            await ctx.send(f"{ctx.message.author.mention}, your " + \
                            "profile currently does not exist in the " + \
                            "database. Create your profile by following " + \
                            "the instructions in /setupprofile")
            return
        
        embed = discord.Embed()
        embed.add_field(name="Questions Rating", value=123.4, inline=False)

        await ctx.send(embed=embed)