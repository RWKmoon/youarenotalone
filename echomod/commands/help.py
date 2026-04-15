import discord
from discord.ext import commands
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="help", description="Mostra todos os comandos do bot")
    async def help(self, interaction: discord.Interaction):
        cmds = """
() Obrigatório [] Opcional 
Comandos disponíveis: 

`/ban @user [razão]` Bane um usuário do servidor

`/kick @user [razão]` Expulsa um usuário do servidor

`/castigar @user (tempo) [razão]` Aplica punição temporária a um usuário

`/mute @user (cargo) [razão]` Aplica mute a um usuário

`/svinfo` Mostra informações do servidor

`/clear (n)` Limpa n mensagens do canal

`/userinfo @user` Mostra informações do usuário

`/addrole @user (@role)` Adiciona um cargo a um usuário

`/nuke` Reseta o canal atual

Use /comando para mais informações sobre um comando específico. (BETA)
"""
        await interaction.response.send_message(cmds)


async def setup(bot):
    await bot.add_cog(Help(bot))
