import os

print ("Seja Bem vindo(a) ao sistema do Zyro")

print("[1] Ligar Zyro Raid")
print("[2] Ligar Zyro Msg")
print("[3] Ligar Zyro Mod")
print("[4] Sair")


opcao = input("Escolha uma opção: ")

if opcao == "1":    
    print("Iniciando Zyro Raid. . .")
elif opcao == "2":
    print("Iniciando Zyro Msg. . .")
elif opcao == "3":
    print("Iniciando Zyro Mod. . .")
elif opcao == "4":
    print("Saindo. . .")
    exit()
else:
    print("Opção invalida")