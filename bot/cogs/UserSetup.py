import discord

from typing import Optional

from discord.ext import commands

from classes.Builders import Builder
from classes.Tags import TagsEnum

from bot.cogs.Views.AddRemoveTagView import AddRemoveTagView

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
    async def setupprofile(self, ctx: commands.Context):
        """
        Instructions on how to set up your profile
        """

        response_str = "To set up your profile, you first need to go to " + \
                        "https://leetcode.com/api/problems/algorithms/. Ensured " + \
                        "that you are logged in and that the \"user_name\" field " + \
                        "at the very start is not empty. Then, save the entire " + \
                        "content as an **.txt** file.\n\nAfterwards, while typing " + \
                        "the /createprofile command, attach that txt file to the " + \
                        "command, and send the message. The server will then save " + \
                        "your information in the database.\n\nIf you would like to " + \
                        "update your information instead, do the same thing, but " + \
                        "with the command /updateprofile.\n\n" + \
                        "By uploading this .txt file, you are agreeing to let LIT " + \
                        "use your personal leetcode statistical data."

        await ctx.send(response_str)

    # TODO: will make a generic settings page with a dropdown menu of all
    # settings, then using that message, edit the message and show the
    # view based on what the user selects
    @commands.hybrid_command()
    async def tagsettings(self, ctx: commands.Context):
        """
        Changes your blacklisted tag settings
        """

        user_result = self.db.find_user(ctx.message.author.id)

        if not user_result:
            await ctx.send(f"{ctx.message.author.mention}, you have not created " +\
                           "a profile yet. You can do so with /createprofile")    
            return

        view = AddRemoveTagView(user_result)

        message = await ctx.send(view=view, ephemeral=True)

        view.message = message

    @commands.hybrid_command()
    async def updateprofile(self, ctx: commands.Context, attachment: Optional[discord.Attachment]):
        """
        Updates your profile, TODO

        Parameters
        -----------
        attachment: discord.Attachment, optional
            Your algorithms txt file
        """
        await ctx.send("TODO")

    @commands.hybrid_command()
    async def createprofile(self, ctx: commands.Context, attachment: discord.Attachment):
        """
        Creates your profile

        Parameters
        -----------
        attachment: discord.Attachment
            Your algorithms txt file
        """

        discord_user_id = ctx.message.author.id
        discord_username = ctx.message.author.name

        attachments = ctx.message.attachments

        # TODO: put all this sanity check in another place
        if self.builder.check_user_exist(discord_user_id):
            await ctx.send(f"{ctx.message.author.mention}, your profile already exists. " + 
                           "If you would like to update your profile instead, use the " +
                           "/updateprofile command.")
            return
        
        file_url = attachments[0]
        file_content = discord_get_attachment_content(file_url)

        self.builder.build_user_data(discord_user_id, discord_username, file_content)

        await ctx.send(f"{ctx.message.author.mention}, your data has been saved to the database.")