print ("Organizador")

print("[1] Compras")
print("[2] Projetos")
print("[3] Ideias")
print("[4] Sair")


opcao = input("Escolha uma opção: ")

if opcao == "1":    
    print("Compras:")
    buy = []
    while True:
        toBuy = input("Oque gostaria de adicionar? (use 'lista' para ver a lista): ")
        if toBuy.lower() == 'lista':
            print(buy)
            exit()
        buy.append(toBuy)
elif opcao == "2":
    print("Projetos: ")
elif opcao == "3":
    print("Ideias: ")
elif opcao == "4":
    print("Saindo. . .")
    exit()
else:
    print("Opção invalida")