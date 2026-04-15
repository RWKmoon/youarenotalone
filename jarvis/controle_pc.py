import psutil
import pyautogui

def fechar_programa(nome):

    for processo in psutil.process_iter():
        try:
            if nome.lower() in processo.name().lower():
                processo.kill()
                print("Programa fechado:", processo.name())
                return True
        except:
            pass

    return False


def mover_mouse():
    pyautogui.moveTo(500, 500, duration=1)


def fechar_aba():
    pyautogui.hotkey("ctrl", "w")