import discord
from discord.ext import commands

from bot.Views.AddRemoveTagView import AddRemoveTagView
from classes.Builders import Builder
from db.db import Database
from utils.utils import discord_get_attachment_content

"""
Contains commands relating to setting up a user profile
"""

class UserSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()

        self.builder: Builder = Builder()

    @commands.hybrid_command()
    async def setup(self, ctx: commands.Context):
        """
        Instructions on how to set up your profile
        """

        response_str = "To set up or update your profile, head to " + \
                        "https://leetcode.com/api/problems/algorithms/. Ensured " + \
                        "that you are **logged in**. Then, copy the entire content of " + \
                        "the webpage by doing **Ctrl-A** and **Ctrl-C**.\n\nAfterwards, " + \
                        "while typing the **/updateprofile** command, paste the output by " + \
                        "doing **Ctrl-V**, and send the message. The server will then save " + \
                        "your leetcode profile information in the database."

        await ctx.send(response_str)

    # TODO: will make a generic settings page with a dropdown menu of all
    # settings, then using that message, edit the message and show the
    # view based on what the user selects
    @commands.hybrid_command()
    async def tagsettings(self, ctx: commands.Context):
        """
        Changes your blacklisted tag settings
        """

        user_result = self.db.find_user_by_discord_id(ctx.message.author.id)

        if not user_result:
            await ctx.send(f"{ctx.message.author.mention}, you have not created " +\
                           "a profile yet. You can do so with /createprofile")    
            return

        view = AddRemoveTagView(user_result)

        message = await ctx.send(view=view, ephemeral=True)

        view.message = message

    @commands.hybrid_command()
    async def updateprofile(self, ctx: commands.Context, attachment: discord.Attachment):
        """
        Creates/updates your profile

        Parameters
        -----------
        attachment: discord.Attachment
            Your algorithms txt file
        """

        discord_user_id = ctx.message.author.id
        discord_username = ctx.message.author.name

        attachments = ctx.message.attachments
        
        file_url = attachments[0]
        file_content = discord_get_attachment_content(file_url)

        if len(file_content) > 100 and file_content[:16] == b'{\"user_name\": \"\"':
            await ctx.send(f"{ctx.message.author.mention}, make sure you are logged in "
                           "before clicking on the link.")
            return

        if self.db.find_user_by_discord_id(discord_user_id):
            self.db.delete_user_by_discord_id(discord_user_id)
        
        self.builder.build_user_data(discord_user_id, discord_username, file_content)

        await ctx.send(f"{ctx.message.author.mention}, your data has been saved to the database.")