from discord.ext import commands

from db.db import Database

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: Database = Database()
    
    @commands.command()
    async def sync(self, ctx: commands.Context):
        # if ctx.author.id == OWNER_USERID:
        #     await bot.tree.sync()
        #     await ctx.send('Command tree synced.')
        # else:
        #     await ctx.send('You must be the owner to use this command!')

        # Fetch existing guild commands and delete them
        # self.bot.tree.clear_commands(guild=ctx.guild)
        # await self.bot.tree.sync(guild=ctx.guild)

        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send('Command tree synced.')

    @commands.hybrid_command()
    async def rating(self, ctx: commands.Context):
        """
        Predicts the rating for a given question
        """
        pass