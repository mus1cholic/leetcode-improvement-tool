import datetime
from discord import Embed, Colour, User

from classes.Tags import TagsEnum

class ProfileEmbed:
    def __init__(self, author: User, user):
        embed = Embed()

        embed.set_author(name=author.name, icon_url=author.display_avatar)
        embed.set_thumbnail(url=user["avatar"])
        embed.color = Colour.blurple()

        embed.title = f"{user['lc_username']}'s Leetcode Profile"
        embed.url = f"https://leetcode.com/u/{user['lc_username']}/"

        embed.add_field(name="Ratings", value="", inline=False)
        embed.add_field(name="Overall Rating", value="{:0.0f}".format(user["projected_rating"]), inline=True)
        embed.add_field(name="Contest Rating", value="{:0.0f}".format(user["contest_rating"]), inline=True)
        embed.add_field(name="Questions Rating", value="{:0.0f}".format(user["questions_rating"]), inline=True)
        embed.add_field(name=chr(173), value=chr(173))

        embed.add_field(name="Skillsets", value="", inline=False)
        for tag in user["tags"]:
            embed.add_field(name=TagsEnum.from_slug(tag["slug"]).full_name,
                            value="{:0.0f}".format(tag["rating"]),
                            inline=True)

        # TODO: put settings not in profile

        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Generated by Leetcode Improvement Tool", icon_url="")

        self.embed = embed