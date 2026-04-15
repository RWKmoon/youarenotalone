import discord
from discord.ext import commands
from discord import app_commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="userinfo", description="Mostra informações do usuário")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        embed = discord.Embed(title="👤 USER INFO", color=0x000000)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="Nome", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Entrou em", value=discord.utils.format_dt(member.joined_at, "F"))

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="svinfo", description="Mostra informações do servidor")
    async def svinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(title="🌐 SERVER INFO", color=0x000000)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Nome", value=guild.name)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Membros", value=guild.member_count)
        embed.add_field(name="Criado em", value=discord.utils.format_dt(guild.created_at, "F"))

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
