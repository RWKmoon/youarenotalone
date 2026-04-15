import webbrowser
import os
from spotify_control import tocar_musica, pausar, despausar, proxima, voltar

def executar(comando):

    if "abrir youtube" in comando:
        webbrowser.open("https://youtube.com")
    
    elif "abrir netflix" in comando:
        webbrowser.open("https://netflix.com")

    elif "abrir google" in comando:
        webbrowser.open("https://google.com")

    elif "abrir download" in comando:
        os.startfile("C:\\Users\\User\\Downloads")

    elif "abrir bloco de notas" in comando:
        os.system("notepad")

    elif "abrir calculadora" in comando:
        os.system("calc")

    elif "abrir chrome" in comando:
        os.system(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    elif "fechar chrome" in comando:
        os.system("taskkill /im chrome.exe /f")

    elif "fechar discord" in comando:
        os.system("taskkill /im Discord.exe /f")

    elif "fechar notepad" in comando:
        os.system("taskkill /im notepad.exe /f")

    elif "fechar calculadora" in comando:
        os.system("taskkill /im Calculator.exe /f")

    elif "fechar tudo" in comando:
        os.system("taskkill /im chrome.exe /f")
        os.system("taskkill /im Discord.exe /f")
        os.system("taskkill /im notepad.exe /f")

    elif "desligar computador" in comando:
        os.system("shutdown /s /t 5")

    elif "abrir" in comando:
        from apps import abrir_app
        if not abrir_app(comando):
            print("App não encontrado")

    elif "pesquise por" in comando:
        termo = comando.replace("pesquise por", "").strip()
        webbrowser.open(f"https://google.com/search?q={termo}")

    elif "tocar musica" in comando:
        musica = comando.replace("tocar musica", "").strip()
        tocar_musica(musica)

    elif "tocar" in comando:
        musica = comando.replace("tocar", "").strip()
        tocar_musica(musica)

    elif "pausar" in comando:
        pausar()

    elif "continuar" in comando:
        despausar()

    elif "proxima" in comando:
        proxima()

    elif "voltar" in comando:
        voltar()

    else:
        print("Comando não reconhecido:", comando)