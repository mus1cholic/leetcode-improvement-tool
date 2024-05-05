from discord.ext import commands

from classes.Builders import Builder
from utils.utils import discord_get_attachment_content

"""
Contains commands relating to setting up a user profile
"""

class UserSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command()
    async def setupprofile(self, ctx: commands.Context):
        # TODO: use an embed eventually

        response_str = "To set up your profile, you first need to go to " + \
                        "https://leetcode.com/api/problems/algorithms/. Ensured " + \
                        "that you are logged in and that the \"user_name\" field " + \
                        "at the very start is not empty. Then, save the entire " + \
                        "content as an **.txt** file.\n\nAfterwards, while typing " + \
                        "the /createprofile command, attach that txt file to the " + \
                        "command, and send the message. The server will then save " + \
                        "your information in the database.\n\nIf you would like to " + \
                        "update your information instead, do the same thing, but " + \
                        "with the command /updateprofile."

        await ctx.send(response_str)

    @commands.hybrid_command()
    async def updateprofile(self, ctx: commands.Context):
        pass

    @commands.hybrid_command()
    async def createprofile(self, ctx: commands.Context):
        discord_user_id = str(ctx.message.author.id)

        user_exists = Builder.check_user_exist(discord_user_id)

        # TODO: put all this sanity check in another place

        if user_exists:
            await ctx.send(f"{ctx.message.author.mention}, your profile already exists." + 
                           "If you would like to update your profile instead, use the " +
                           "/updateprofile command.")
            return
        
        attachments = ctx.message.attachments

        if not attachments:
            await ctx.send(f"{ctx.message.author.mention}, please attach your txt file " +
                           "as instructed in /setupprofile.")
            return
        
        if len(attachments) > 1:
            await ctx.send(f"{ctx.message.author.mention}, please only include one " +
                           "attachment.")
            return
        
        file_url = attachments[0]
        file_content = discord_get_attachment_content(file_url)

        Builder.build_user_data(discord_user_id, file_content)

        await ctx.send(f"{ctx.message.author.mention}, your data has been saved to the database.")