import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="72042a9d606b4d8992d5f1ee2e87bd5b",
    client_secret="969be0904df14736a601b278d0e9e396",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

def tocar_musica(nome):
    results = sp.search(q=nome, type="track", limit=1)

    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        sp.start_playback(uris=[track["uri"]])
        print(f"Tocando: {track['name']} - {track['artists'][0]['name']}")
    else:
        print("Música não encontrada.")

def pausar():
    sp.pause_playback()

def despausar():
    sp.start_playback()

def proxima():
    sp.next_track()

def voltar():
    sp.previous_track()

def volume(valor):
    sp.volume(valor)

def musica_info():

    playback = sp.current_playback()

    if playback and playback["item"]:

        nome = playback["item"]["name"]
        artista = playback["item"]["artists"][0]["name"]

        capa = playback["item"]["album"]["images"][0]["url"]

        progresso = playback["progress_ms"]
        duracao = playback["item"]["duration_ms"]

        volume = playback["device"]["volume_percent"]

        return {
            "titulo": nome,
            "artista": artista,
            "capa": capa,
            "progresso": progresso,
            "duracao": duracao,
            "volume": volume
        }

    return None