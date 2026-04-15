import os
import shutil
from pathlib import Path

# Defina sua pasta de downloads
DOWNLOADS_DIR = str(Path.home() / "Downloads")

# Categorias e extensões
CATEGORIES = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Vídeos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Áudios": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
    "Documentos": [".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".txt"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executáveis": [".exe", ".msi", ".sh", ".apk"],
    "Outros": []
}

def mover_arquivos():
    for arquivo in os.listdir(DOWNLOADS_DIR):
        caminho_arquivo = os.path.join(DOWNLOADS_DIR, arquivo)

        if os.path.isfile(caminho_arquivo):
            _, ext = os.path.splitext(arquivo)
            ext = ext.lower()

            destino_categoria = "Outros"
            for categoria, extensoes in CATEGORIES.items():
                if ext in extensoes:
                    destino_categoria = categoria
                    break

            pasta_destino = os.path.join(DOWNLOADS_DIR, destino_categoria)
            os.makedirs(pasta_destino, exist_ok=True)

            shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
            print(f"Movido: {arquivo} → {destino_categoria}")

if __name__ == "__main__":
    mover_arquivos()
    print("Organização concluída!")