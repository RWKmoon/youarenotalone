import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta


class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # MUTE (timeout)
    @app_commands.command(name="mute", description="Aplica timeout em um usuário")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, tempo: int, reason: str = "Não informado"):
        await interaction.response.defer()

        until = discord.utils.utcnow() + timedelta(minutes=tempo)
        await member.edit(timed_out_until=until, reason=reason)

        embed = discord.Embed(title="🔇 MUTE", color=0x000000)
        embed.add_field(name="Usuário", value=member.mention)
        embed.add_field(name="Aplicador", value=interaction.user.mention)
        embed.add_field(name="Tempo", value=f"{tempo} min")
        embed.add_field(name="Motivo", value=reason, inline=False)

        await interaction.followup.send(embed=embed)


    # ADDROLE
    @app_commands.command(name="addrole", description="Adiciona um cargo a um usuário")
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await interaction.response.defer()

        await member.add_roles(role)

        embed = discord.Embed(title="➕ CARGO ADICIONADO", color=0x000000)
        embed.add_field(name="Usuário", value=member.mention)
        embed.add_field(name="Cargo", value=role.mention)
        embed.add_field(name="Aplicador", value=interaction.user.mention)

        await interaction.followup.send(embed=embed)


    # CLEAR
    @app_commands.command(name="clear", description="Limpa mensagens do canal")
    async def clear(self, interaction: discord.Interaction, quantidade: int):
        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=quantidade)

        await interaction.followup.send(f"🧹 {len(deleted)} mensagens apagadas.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderacao(bot))
