from discord.ext import commands

class Recommendations(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def sync(self, ctx):
        # print("sync command")
        # if ctx.author.id == OWNER_USERID:
        #     await bot.tree.sync()
        #     await ctx.send('Command tree synced.')
        # else:
        #     await ctx.send('You must be the owner to use this command!')

        await self.bot.tree.sync()
        await ctx.send('Command tree synced.')

        print(self.bot.tree.get_commands())

    @commands.hybrid_command()
    async def recommend(self, ctx):
        await ctx.send("TODO")