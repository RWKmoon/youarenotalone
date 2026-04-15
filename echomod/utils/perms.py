from discord import Interaction

async def check_perm(interaction: Interaction, perm: str):
    perms = interaction.user.guild_permissions

    if not getattr(perms, perm, False):
        await interaction.response.send_message(
            "❌ Você não tem permissão para usar este comando.",
            ephemeral=True
        )
        return False

    return True
