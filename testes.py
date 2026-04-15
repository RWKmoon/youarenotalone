import time
import random
import spotipy
from colorama import Fore
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="72042a9d606b4d8992d5f1ee2e87bd5b",
    client_secret="969be0904df14736a601b278d0e9e396",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))
    
sp.start_playback()

a = "E so agora"

for j in a:
    print(j, end="", flush=True)
    time.sleep(random.uniform(0.05, 0.2))
print(" ")
    
time.sleep(2.5)
    
b = "O homem chora"

for k in b:
    print(k, end="", flush=True)
    time.sleep(random.uniform(0.05, 0.2))
print(" ")

time.sleep(1.5)

c = "E quando o homem chora"
for l in c:
    print(l, end="", flush=True)
    time.sleep(random.uniform(0.05, 0.2))
print(" ")

time.sleep(1.5)

d = "Precisa pedir o seu..."
for m in d:
    print(m, end="", flush=True)
    time.sleep(random.uniform(0.05, 0.2))
print(" ")

time.sleep(1)

e = "Chora"
for n in e:
    print(Fore.RED + n, end="", flush=True)
    time.sleep(random.uniform(0.05, 0.2))
print(" ")
