import pyautogui
import time
import string

# --- Configuração ---
# Tempo para clicar onde você quer digitar após rodar o script
tempo_espera = 3 
# Intervalo entre as letras (0 = o mais rápido possível)
intervalo_letras = 0.02

print(f"Clique no campo de texto em {tempo_espera} segundos...")
time.sleep(tempo_espera)

# Gera o alfabeto minúsculo (abcdefghijklmnopqrstuvwxyz)
alfabeto = string.ascii_lowercase

# Digita o alfabeto
# O parâmetro 'interval' define o atraso entre cada tecla
pyautogui.write(alfabeto, interval=intervalo_letras)

print("Alfabeto digitado!")
