from discord.ext import commands
import time

from .cogs.Recommendations import Recommendations
from .cogs.UserSetup import UserSetup
from .cogs.Profile import Profile

class Bot(commands.Bot):
    async def on_ready(self):
        start_time = time.perf_counter()

        await self.add_cogs()

        end_time = time.perf_counter()

        print(f'Logged in as {self.user} (ID: {self.user.id}), took {end_time - start_time}s')
        print('------')

    async def add_cogs(self):
        await self.add_cog(UserSetup(self))
        await self.add_cog(Recommendations(self))
        await self.add_cog(Profile(self))