import time
import winsound
import threading
import os
from xmlrpc import client
import openai
from colorama import Fore, Style, init, Back

def sound():
    winsound.PlaySound("audio", winsound.SND_ALIAS)

with open("mensagem1.txt", "w", encoding="utf-8") as f:
    f.write("")

with open("mensagem.txt", "w", encoding="utf-8") as f:
            f.write('''Ola, seu sistema foi infectado pelo echo, um malware de acesso remoto (RAT) criado por l9viego.
    O echo é capaz de roubar informações, controlar o sistema e executar comandos remotamente.
    Se você está lendo isso, significa que seus arquivos foram comprometidos.
    Por favor, tome medidas imediatas para remover o malware e proteger seus dados.''')

print("════════════════════ஜ۩۞۩ஜ═════════════════════")

print (f"Press 'S' to start . . .")
opc1 = input("➜").lower()
if opc1 == "s":
    for i in range(11):
        time.sleep(0.05)
        os.startfile("mensagem.txt")

