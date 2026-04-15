import time
import winsound
import threading
import os
from colorama import Fore, Style, init, Back

def sound():
    winsound.PlaySound("Som-de-SUSSURROS-ASSUSTADORES-Som-na-Mente-_youtube_.wav", winsound.SND_ALIAS)


print("=============You are an idiot!=============")  
time.sleep(1)
print("Calculating. . .")
time.sleep(3)
print("Exporting your files to the echo system. . .")
time.sleep(2)
print("Running the echo system. . .")

print(f"{Fore.GREEN}Loading{'.'}{Style.RESET_ALL}")

for i in range(21):
    time.sleep(0.05)
    os.startfile("mensagem.txt")
