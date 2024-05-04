from discord.ext import commands
import asyncio

from .cogs.Recommendations import Recommendations

class Bot(commands.Bot):
    async def on_ready(self):
        await self.add_cogs()

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def add_cogs(self):
        await self.add_cog(Recommendations(self))