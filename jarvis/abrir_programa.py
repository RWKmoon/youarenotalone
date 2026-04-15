import subprocess

def abrir_programa(nome):

    try:
        subprocess.Popen(nome)
        print(f"Abrindo {nome}")
        return True
    except:
        return False