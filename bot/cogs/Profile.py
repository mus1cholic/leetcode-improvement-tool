from discord.ext import commands
from typing import Optional

from bot.Embeds.ProfileEmbed import ProfileEmbed
from db.db import Database

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()

    @commands.hybrid_command()
    async def profile(self, ctx: commands.Context, lc_username: Optional[str]):
        """
        View your Leetcode profile and various statistics

        Parameters
        -----------
        lc_username: str, optional
            an optional parameter to check the profile of others
        """

        discord_user_id = ctx.message.author.id
        author = ctx.message.author

        if lc_username:
            user = self.db.find_user_by_leetcode_username(lc_username)

            if not user:
                await ctx.send(f"{author.mention}, the " + \
                                "profile you are trying to look for does not exist in the " + \
                                "database. Please make sure they have already registered, " + \
                                "or check your spelling")
                return
        else:
            user = self.db.find_user_by_discord_id(discord_user_id)

            if not user:
                await ctx.send(f"{author.mention}, your " + \
                                "profile currently does not exist in the " + \
                                "database. Create your profile by following " + \
                                "the instructions in /setupprofile")
                return
        
        profile_embed = ProfileEmbed(author, user)

        await ctx.send(embed=profile_embed.embed)