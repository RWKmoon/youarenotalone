import discord, os
from discord.ext import commands

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Bot(commands.Bot):
    async def setup_hook(self):
        commands_path = os.path.join(BASE_DIR, "commands")

        print("PASTA BASE:", BASE_DIR)
        print("PASTA COMMANDS:", commands_path)

        for file in os.listdir(commands_path):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(f"commands.{file[:-3]}")

        await self.tree.sync()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = Bot(command_prefix="/", intents=intents)
