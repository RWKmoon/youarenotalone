import os

apps = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "discord": r"C:\Users\User\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "notepad": "notepad",
    "calculadora": "calc"
}

def abrir_app(nome):

    for app in apps:
        if app in nome:
            os.system(apps[app])
            print("Abrindo", app)
            return True

    return False