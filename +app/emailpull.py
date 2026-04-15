import random
import string
import json
import os
import time
import requests

def gerar_senha(tamanho=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def gerar_emails_temp(qtd=10):
    dominios = ["1secmail.com", "1secmail.net", "1secmail.org"]
    dados = []

    for _ in range(qtd):
        nome = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        dominio = random.choice(dominios)
        email = f"{nome}@{dominio}"
        senha = gerar_senha()
        dados.append({
            "email": email,
            "login": nome,
            "dominio": dominio,
            "senha": senha
        })

    return dados

def salvar_em_json(dados, pasta="emails_temp", nome_arquivo="emails.json"):
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome_arquivo)
    with open(caminho, "w") as f:
        json.dump(dados, f, indent=4)
    print(f"[✔] Emails salvos em: {caminho}")

def consultar_caixa_entrada(email_obj):
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_obj['login']}&domain={email_obj['dominio']}"
    try:
        resp = requests.get(url).json()
        return resp
    except Exception as e:
        print(f"Erro ao consultar {email_obj['email']}: {e}")
        return []

def ler_conteudo_email(email_obj, msg_id):
    url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_obj['login']}&domain={email_obj['dominio']}&id={msg_id}"
    try:
        resp = requests.get(url).json()
        return resp
    except Exception as e:
        print(f"Erro ao ler conteúdo do e-mail {email_obj['email']}, ID {msg_id}: {e}")
        return {}

def mostrar_emails_recebidos(dados_emails):
    for email in dados_emails:
        print(f"\n📬 Caixa de entrada de {email['email']}:")
        mensagens = consultar_caixa_entrada(email)
        if not mensagens:
            print("  (vazia)")
        else:
            for msg in mensagens:
                print(f"  - De: {msg['from']} | Assunto: {msg['subject']} | ID: {msg['id']}")
                conteudo = ler_conteudo_email(email, msg['id'])
                corpo = conteudo.get('textBody') or conteudo.get('htmlBody') or "(sem conteúdo)"
                print(f"    📄 Conteúdo:\n{corpo.strip()[:300]}")  # Mostra até 300 caracteres

# Executar
emails = gerar_emails_temp()
salvar_em_json(emails)
print("\n⏳ Aguardando 10 segundos antes de verificar a caixa de entrada...\n")
time.sleep(10)  # Simula tempo para alguém enviar e-mails
mostrar_emails_recebidos(emails)

