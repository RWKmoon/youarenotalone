import discord, asyncio
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="nuke", description="Reseta canal")
    async def nuke(self, interaction: discord.Interaction):
        canal = interaction.channel
        clone = await canal.clone()
        await canal.delete()
        await clone.send("Canal resetado.")


async def setup(bot):
    await bot.add_cog(Util(bot))
