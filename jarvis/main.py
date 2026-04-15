import threading
from voz import ouvir
from comandos import executar
from interface import iniciar_interface

# inicia interface em thread separada
interface_thread = threading.Thread(target=iniciar_interface)
interface_thread.daemon = True
interface_thread.start()

# loop da voz
while True:

    comando = ouvir()

    if "jarvis" in comando:

        comando = comando.replace("jarvis", "").strip()

        print("Comando:", comando)

        executar(comando)