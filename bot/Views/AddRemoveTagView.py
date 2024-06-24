import discord
from discord.ui import View, Button
from functools import partial

from classes.Tags import TagsEnum
from db.db import Database

class AddRemoveTagView(View):
    def __init__(self, user_result, timeout=30):
        super().__init__(timeout=timeout)

        # get the results of settings
        self.db = Database()
        self.user_db_id = user_result['_id']
        self.blacklisted_tags = [TagsEnum.from_slug(slug) for slug in user_result["settings"]["blacklisted_tags"]]

        self.message = None

        for i, tag in enumerate(TagsEnum):
            if tag in self.blacklisted_tags:
                button = Button(label=tag.full_name, style=discord.ButtonStyle.red)
            else:
                button = Button(label=tag.full_name, style=discord.ButtonStyle.green)

            button.callback = partial(self.tag_callback, button, tag)
            button.row = i // 5
            self.add_item(button)

        # Button to submit final choices
        self.submit_button = Button(label="Save Tag Filters", style=discord.ButtonStyle.primary)
        self.submit_button.callback = self.submit_callback
        self.submit_button.row = 1 + (1 + i) // 5
        self.add_item(self.submit_button)

    async def tag_callback(self, button: Button, tag: TagsEnum, interaction: discord.Interaction):
        if tag in self.blacklisted_tags:
            self.blacklisted_tags.remove(tag)
            button.style = discord.ButtonStyle.green
        else:
            self.blacklisted_tags.append(tag)
            button.style = discord.ButtonStyle.red

        await interaction.response.edit_message(view=self)

    async def submit_callback(self, interaction: discord.Interaction):
        field_name = "settings"
        field_val = {
            "blacklisted_tags": self.blacklisted_tags
        }

        result = self.db.update_user_field(self.user_db_id, field_name, field_val)

        if result == None:
            await interaction.response.send_message(f"Database error occured", ephemeral=True)

            return

        await interaction.response.send_message(f"Your settings have been updated. " + \
                                                "You will now not see the following tags " + \
                                                "when you get recommended a problem: " + \
                                                f"{', '.join(self.blacklisted_tags)}",
                                                ephemeral=True)
        self.stop()

    async def on_timeout(self):
        # This method is called when the view times out
        for item in self.children:
            item.disabled = True  # Disable all components

        await self.message.delete()