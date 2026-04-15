import requests
import random
import time
import os
import sys
import string
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

MAX_USERNAMES = 200
DELAY = 1.0
MAX_RETRIES = 5

CHARS = string.ascii_lowercase + string.digits
session = requests.Session()

class C:
    R="\033[0m"; G="\033[92m"; RED="\033[91m"; Y="\033[93m"; B="\033[1m"

def now():
    return datetime.now().strftime("%H:%M:%S")

def gen():
    return ''.join(random.choices(CHARS, k=random.randint(10,20)))

def log(user, status):
    if status == "available":
        print(f"{C.B}[{now()}]{C.R} {user:<6} | {C.G}✔ DISPONÍVEL{C.R}")
    elif status == "taken":
        print(f"{C.B}[{now()}]{C.R} {user:<6} | {C.RED}✖ OCUPADO{C.R}")
    else:
        print(f"{C.B}[{now()}]{C.R} {user:<6} | {C.Y}⚠ PULADO{C.R}")
    
    sys.stdout.flush()

def check(user):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

    for _ in range(MAX_RETRIES):
        try:
            r = session.post(url, json={"username": user}, timeout=10)

            if r.status_code == 429:
                retry = r.json().get("retry_after", 2)
                time.sleep(retry)
                continue

            if r.status_code == 200:
                if r.json().get("taken"):
                    log(user, "taken")
                else:
                    log(user, "available")
                return

        except:
            time.sleep(1)

    # se falhou tudo
    log(user, "skip")

def main():
    os.system("cls" if os.name=="nt" else "clear")
    print("⚡ USERNAME CHECKER (FIXED)\n")

    with ThreadPoolExecutor(max_workers=2) as ex:
        for i in range(MAX_USERNAMES):
            u = gen()
            print(f"Testando {i+1}/{MAX_USERNAMES}...", end="\r")
            ex.submit(check, u)
            time.sleep(DELAY)

    print("\n\nFinalizado.")

if __name__ == "__main__":
    main()