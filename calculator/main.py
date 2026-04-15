from utils import get_numbers, get_operation

print ("Calculadora Fodastica")
print ("-------------------")

n1, n2 = get_numbers()

op = get_operation()
if op  == "+":
    resultadomais = n1 + n2
    print (f"{resultadomais}")
elif op == "-":
    resultadomenos = n1 - n2
    print (f"{resultadomenos}")
elif op == "*":
    resultadovezes = n1 * n2
    print (f"{resultadovezes}")
elif op == "/":
    resultadodivisao = n1 / n2
    if n2 != 0:
        print (f"{resultadodivisao}")
    else:
        print ("Erro: Divisão por zero não é permitida.")
else:
    print ("Operação inválida.")
