# Para qualquer duvida ou suporte entre em contato com o Discord: iownyouhz
# Bot desenvolvido por "yMoon"



import discord
from datetime import timedelta
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# HELP
@bot.tree.command(name="help", description="Mostra todos os comandos do bot")
async def help(interaction: discord.Interaction):
    cmds = """
    `/ban @user [razão]` • bane um membro  
    `/castigar @user [cargo] [razão]` • castiga (kick + mute temporário)  
    `/mute @user [cargo] [razão]` • atribui role de mute  
    `/svinfo` • mostra informações do servidor  
    `/clear [n]` • deleta as últimas n mensagens  
    `/mod on/off` • ativa/desativa moderação automática  
    `/userinfo @user` • mostra informações do usuário  
    `/addrole @user @role` • adiciona um cargo a um usuário
    """
    await interaction.response.send_message(cmds)

# --- CONFIRMATION BUTTON VIEW ---
class ConfirmView(discord.ui.View):
    def __init__(self, author, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("❌ Você não pode interagir com esses botões.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Sim", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()
        await interaction.response.defer()  # apenas para não enviar mensagem agora

    @discord.ui.button(label="❌ Não", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()
        await interaction.response.defer()


# BAN
@bot.tree.command(name="ban", description="Bane um usuário")
@app_commands.describe(member="Usuário que será banido", reason="Motivo do ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Não informada"):
    view = ConfirmView(interaction.user)
    msg = await interaction.response.send_message(
        f"⚠️ Você tem certeza que deseja banir {member.mention}?\nMotivo: {reason}", delete_after=5,
        view=view
    )
    await view.wait()
    if view.value is None or view.value is False:
        await interaction.followup.send("❌ Ação cancelada.", ephemeral=True)
        return
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="PUNIDO(A)",
            description="Banido(a)",
            color=0x000000
        )
        embed.set_author(name="Echo")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1426339111920341052/1426339240907640904/image.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1430299544234758145/1430964703655497922/remove.png")
        embed.add_field(name="Aplicador: ", value=interaction.user.mention, inline=False)
        embed.add_field(name="Punido: ", value=member.mention, inline=True)
        embed.add_field(name="Motivo: ", value=reason, inline=False)
        await interaction.followup.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send("❌ Não tenho permissão para banir este usuário.", ephemeral=True)


# CASTIGAR
@bot.tree.command(name="castigar", description="Aplica timeout a um usuário e envia embed (tempo em minutos).")
@app_commands.describe(member="Usuário a ser castigado", tempo="Tempo em minutos", reason="Motivo")
async def castigar(interaction: discord.Interaction, member: discord.Member, tempo: int = 10, reason: str = "Não informada"):
    # checagem mínima de permissão do bot
    if not interaction.guild.me.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ Eu preciso da permissão `Moderate Members` para castigar usuários.", ephemeral=True)
        return

    # não aplicar ao dono do servidor
    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ Não posso aplicar punição ao dono do servidor.", ephemeral=True)
        return

    await interaction.response.defer()  # evita timeout enquanto aplica a ação
    try:
        until = discord.utils.utcnow() + timedelta(minutes=tempo)
        await member.edit(timed_out_until=until, reason=f"Punição por {interaction.user} — Motivo: {reason}")

    except discord.Forbidden:
        await interaction.followup.send("❌ Falha: permissões insuficientes ou hierarquia impede a ação.", ephemeral=True)
        return
    except discord.HTTPException as e:
        await interaction.followup.send(f"❌ Erro ao aplicar timeout: {e}", ephemeral=True)
        return

    embed = discord.Embed(
        title="PUNIDO(A)",
        description=f"Timeout aplicado por {tempo} minuto(s).",
        color=0x000000
    )
    embed.set_author(name="Echo")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1426339111920341052/1426339240907640904/image.png")    
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1430299544234758145/1430964703655497922/remove.png")
    embed.add_field(name="Aplicador:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Punido:", value=member.mention, inline=True)
    embed.add_field(name="Motivo:", value=reason, inline=False)
    embed.add_field(name="Duração:", value=f"{tempo} minuto(s)", inline=False)

    await interaction.followup.send(embed=embed)

# MUTE
@bot.tree.command(name="mute", description="Mutar um usuário atribuindo um cargo de mute")
@app_commands.describe(member="Usuário que será mutado", role="Cargo de mute", reason="Motivo do mute")
async def mute(interaction: discord.Interaction, member: discord.Member, role: discord.Role, reason: str = "Não informada"):
    view = ConfirmView(interaction.user)
    msg = await interaction.response.send_message(
        f"⚠️ Você tem certeza que deseja mutar {member.mention}?\nCargo: {role.mention}\nMotivo: {reason}", delete_after=5,
        view=view
    )
    await view.wait()
    if view.value is None or view.value is False:
        await interaction.followup.send("❌ Ação cancelada.", ephemeral=True)
        return
    try:
        await member.add_roles(role)
        embed = discord.Embed(
            title="PUNIDO(A)",
            description="Mutado(a)",
            color=0x000000
        )
        embed.set_author(name="Echo")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1426339111920341052/1426339240907640904/image.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1430299544234758145/1430964703655497922/remove.png")
        embed.add_field(name="Aplicador: ", value=interaction.user.mention, inline=True)
        embed.add_field(name="Punido: ", value=member.mention, inline=True)
        embed.add_field(name="Cargo adicionado: ", value=role.mention, inline=False)
        embed.add_field(name="Motivo: ", value=reason, inline=False)
        await interaction.followup.send(embed=embed)
    except discord.Forbidden:
        await interaction.followup.send("❌ Não consegui adicionar o cargo.", ephemeral=True)


# ADD ROLE
@bot.tree.command(name="addrole", description="Adiciona um cargo a um usuário")
@app_commands.describe(member="Usuário que receberá o cargo", role="Cargo a ser adicionado")
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    view = ConfirmView(interaction.user)
    msg = await interaction.response.send_message(
        f"⚠️ Você tem certeza que deseja adicionar {role.mention} para {member.mention}?",
        view=view,
        ephemeral=True
    )
    await view.wait()
    if view.value is None or view.value is False:
        await interaction.followup.send("❌ Ação cancelada.", ephemeral=True)
        return
    try:
        await member.add_roles(role)
        await interaction.followup.send(f"✅ Cargo {role.name} adicionado para {member.mention}!", ephemeral=True)
    except discord.Forbidden:
        await interaction.followup.send("❌ Não tenho permissão para adicionar este cargo.", ephemeral=True)


# --- Comandos restantes (mantidos iguais) ---

# CLEAR
@bot.tree.command(name="clear", description="Deleta as últimas n mensagens")
@app_commands.describe(n="Quantidade de mensagens")
async def clear(interaction: discord.Interaction, n: int = 100):
    await interaction.channel.purge(limit=n+1)
    msg = await interaction.channel.send(f"{n} mensagens foram apagadas.")
    await asyncio.sleep(5)
    await msg.delete()

# SERVER INFO
@bot.tree.command(name="svinfo", description="Mostra informações do servidor")
async def svinfo(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(
        title="Server Info",
        color=0x000000
    )
    embed.set_author(name="Echo")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1426339111920341052/1426339240907640904/image.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1430299544234758145/1430964703655497922/remove.png")
    embed.add_field(name="Membros", value=g.member_count)
    embed.add_field(name="Criado em", value=g.created_at.strftime("%d/%m/%Y"))
    await interaction.response.send_message(embed=embed)

# USER INFO
@bot.tree.command(name="userinfo", description="Mostra informações de um usuário")
@app_commands.describe(member="Usuário a ser verificado")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(
        title=str(member.name),
        description=(f"Mention: {member.mention}"),
        color=0x000000
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1426339111920341052/1426339240907640904/image.png")
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Tag", value=member)
    embed.add_field(name="ID: ", value=member.id, inline=True)
    embed.add_field(name="Entrou em: ", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=False)
    embed.add_field(name="Criado em: ", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
    embed.add_field(name="Status: ", value=str(member.status).title(), inline=True)
    if member.voice and member.voice.channel:
        embed.add_field(name="Canal de voz ativo: ", value=member.voice.channel.name)
    else:
        embed.add_field(name="Canal de voz", value="Não está em nenhum canal")
    roles = [r.mention for r in member.roles[1:]]
    embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join(roles) or "Nenhum", inline=False)
    await interaction.response.send_message(embed=embed)

# NUKE
@bot.tree.command(name="nuke", description="Duplica o canal atual e deleta o original")
async def nuke(interaction: discord.Interaction):
    canal_original = interaction.channel
    clone = await canal_original.clone(
        name=canal_original.name,
        reason=f"Reset de canal solicitado por {interaction.user}"
    )
    await clone.edit(category=canal_original.category, position=canal_original.position)
    await clone.send(f"Canal resetado por {interaction.user.mention}.")
    await canal_original.delete(reason=f"Reset solicitado por {interaction.user}")


# ON READY
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot On como {bot.user}")



bot.run("MTQ2MDczNjgzNjAyMzM1NzUwMw.Gr4gts.hFb8Cy394_oioeNXjir-bLJ_9aM-oEfJP5fvCo")
