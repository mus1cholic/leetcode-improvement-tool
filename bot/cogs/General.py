from discord.ext import commands

from db.db import Database
from utils.constants import DISCORD_OWNER_ID

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()
    
    @commands.command()
    async def sync(self, ctx: commands.Context):
        if ctx.author.id != DISCORD_OWNER_ID:
            return
        
        # delete commands
        # self.bot.tree.clear_commands(guild=ctx.guild)
        # await self.bot.tree.sync(guild=ctx.guild)

        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)

        await ctx.send('Command tree synced.')

    @commands.hybrid_command()
    async def question(self, ctx: commands.Context):
        """
        Returns the generic info for a question, including rating
        """
        pass