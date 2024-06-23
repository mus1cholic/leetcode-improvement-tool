from discord.ui import View, Select, Button, Modal
import discord

from db.db import Database

from classes.Tags import TagsEnum

from classes.Suggestions import AdvancedSuggestion

class RangeModal(Modal, title="Rating Range"):
    def __init__(self, parent_view):
        super().__init__()

        self.parent_view = parent_view

        self.add_item(discord.ui.TextInput(
            label="Minimum Value",
            style=discord.TextStyle.short,
            placeholder="Enter minimum value...",
            required=True
        ))
        self.add_item(discord.ui.TextInput(
            label="Maximum Value",
            style=discord.TextStyle.short,
            placeholder="Enter maximum value...",
            required=True
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            min_val = int(self.children[0].value)
            max_val = int(self.children[1].value)

            if min_val > max_val:
                await interaction.response.send_message("Minimum value must be less than maximum value.", ephemeral=True)
            else:
                self.parent_view.min_rating = min_val
                self.parent_view.max_rating = max_val

                await interaction.response.send_message(f"Rating range set from {min_val} to {max_val}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Please enter valid integer values.", ephemeral=True)

class SearchTermModal(Modal, title="Search Term"):
    def __init__(self, parent_view):
        super().__init__()

        self.parent_view = parent_view

        self.add_item(discord.ui.TextInput(
            label="Search Term",
            style=discord.TextStyle.short,
            placeholder="Enter search term...",
            required=True
        ))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            search_term = self.children[0].value

            self.parent_view.search_term = search_term

            await interaction.response.send_message(f"Search term set to \"{search_term}\"", ephemeral=True)
        except ValueError:
            pass

class AdvancedRecommendView(View):
    def __init__(self, discord_user_id: int, db: Database, timeout=60):
        super().__init__(timeout=timeout)

        self.min_rating = None
        self.max_rating = None
        self.search_term = None
        self.must_include_selected_options = []
        self.ignore_selected_options = []

        self.advanced_suggestion: AdvancedSuggestion = AdvancedSuggestion()
        self.discord_user_id = discord_user_id
        user_result = db.find_user_by_discord_id(discord_user_id)
        self.user_blacklisted_tags = [TagsEnum.from_slug(slug) for slug in user_result["settings"]["blacklisted_tags"]]
        # self.ignore_selected_options = self.user_blacklisted_tags
        self.ignore_selected_options = [tag.value for tag in self.user_blacklisted_tags]

        self.add_components()

        self.message = None

    def add_components(self):
        # must include tag component
        options = [
            discord.SelectOption(
                label=choice.full_name,
                value=choice.value
            ) for choice in TagsEnum
        ]

        self.tags_must_include_select = discord.ui.Select(
            placeholder="Select tags to MUST include",
            min_values=0,
            max_values=len(TagsEnum),
            options=options,
            row=1
        )

        self.tags_must_include_select.callback = self.must_include_callback
        self.add_item(self.tags_must_include_select)

        # ignore tag component
        options = [
            discord.SelectOption(
                label=choice.full_name,
                value=choice.value,
                default=choice in self.user_blacklisted_tags
            ) for choice in TagsEnum
        ]

        self.tags_ignore_select = discord.ui.Select(
            placeholder="Select tags to ignore",
            min_values=0, 
            max_values=len(TagsEnum),  # Allow selecting multiple options up to the number of enum values
            options=options,
            row=2
        )

        self.tags_ignore_select.callback = self.ignore_callback
        self.add_item(self.tags_ignore_select)

    @discord.ui.button(label="Set Rating Range", style=discord.ButtonStyle.primary, row=0)
    async def set_range(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RangeModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Set Search Term", style=discord.ButtonStyle.primary, row=0)
    async def set_search_term(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SearchTermModal(self)
        await interaction.response.send_modal(modal)

    async def must_include_callback(self, interaction: discord.Interaction):
        self.must_include_selected_options = self.tags_must_include_select.values
        await interaction.response.defer()

    async def ignore_callback(self, interaction: discord.Interaction):
        self.ignore_selected_options = self.tags_ignore_select.values
        await interaction.response.defer()

    @discord.ui.button(label="Recommend", style=discord.ButtonStyle.green, row=3)
    async def confirm(self, interaction: discord.Interaction, button: Button):  
        self.stop()
        await self.on_timeout()

        response = self.advanced_suggestion.suggest_problem(self.discord_user_id,
                                                            min_rating=self.min_rating,
                                                            max_rating=self.max_rating,
                                                            search_term=self.search_term,
                                                            tags_must_include=self.must_include_selected_options,
                                                            tags_ignore=self.ignore_selected_options)
        
        response = f"{interaction.user.mention}, {response}"

        await interaction.response.send_message(response)

    async def on_timeout(self):
        # This method is called when the view times out
        for item in self.children:
            item.disabled = True  # Disable all components

        await self.message.delete()