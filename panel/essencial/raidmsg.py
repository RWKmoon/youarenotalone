import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK = os.getenv("WEBHOOK")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class RaidButton(discord.ui.View):
    def __init__(self, author: discord.User):
        super().__init__(timeout=None)
        self.author = author

    @discord.ui.button(label="Iniciar Raid", style=discord.ButtonStyle.danger)
    async def start_raid(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("Você não tem permissão para usar este botão!", ephemeral=True)
            return

        await interaction.response.send_message("Enviando mensagens...")

        for i in range(10):
            await asyncio.sleep(0,1)
            await interaction.followup.send(content="# VIELA TA NA CASA # discord.gg/viela                                                                                                                                             # VIELA)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            @everyone")

@tree.command(name="raid", description="Mostra um botão para iniciar o envio das mensagens.")
async def raid(interaction: discord.Interaction):
    view = RaidButton(interaction.user)
    await interaction.response.send_message("Clique abaixo e deixe acontecer:", view=view, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {client.user}")

client.run(f"{WEBHOOK}")





# BOT OWNED BY: MOON