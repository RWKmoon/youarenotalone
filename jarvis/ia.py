def responder(pergunta):

    respostas = {
        "quem é você": "Eu sou o Jarvis",
        "bom dia": "Bom dia!",
        "boa noite": "Boa noite!",
        "como você está": "Estou funcionando perfeitamente"
    }

    for chave in respostas:
        if chave in pergunta:
            return respostas[chave]

    return "Ainda estou aprendendo."