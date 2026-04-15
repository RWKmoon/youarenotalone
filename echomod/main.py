from core.bot import bot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)