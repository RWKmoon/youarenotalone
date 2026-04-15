import discord
from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print(f"Online como {self.bot.user}")

async def setup(bot):
    await bot.add_cog(Ready(bot))