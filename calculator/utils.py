def get_numbers():
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    return n1, n2

def get_operation():
    print ("+ - Soma")
    print ("- - Subtração")
    print ("* - Multiplicação")
    print ("/ - Divisão")
    op = input("Digite a operação desejada: ")
    return op