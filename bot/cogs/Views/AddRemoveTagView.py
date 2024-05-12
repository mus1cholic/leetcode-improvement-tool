from discord.ui import View, Button
import discord

from classes.Tags import TagsEnum

from functools import partial

class AddRemoveTagView(View):
    def __init__(self, *options, timeout=30):
        super().__init__(timeout=timeout)
        self.selected_options = []
        self.message = None

        for (i, tag) in enumerate(TagsEnum):
            button = Button(label=tag.name, style=discord.ButtonStyle.green)
            button.callback = partial(self.tag_callback, tag)
            button.row = i // 5
            self.add_item(button)

        # Button to submit final choices
        self.submit_button = Button(label="Save Tag Filters", style=discord.ButtonStyle.primary)
        self.submit_button.callback = self.submit_callback
        self.submit_button.row = 1 + (1 + i) // 5
        self.add_item(self.submit_button)

    async def tag_callback(self, tag: TagsEnum, interaction: discord.Interaction):
        print(tag)

        await interaction.response.send_message(f"Added", ephemeral=True)

    async def submit_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Final selections: {', '.join(self.selected_options)}", ephemeral=False)
        self.stop()

    async def on_timeout(self):
        # This method is called when the view times out
        for item in self.children:
            item.disabled = True  # Disable all components

        await self.message.delete()