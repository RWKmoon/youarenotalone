data = input("Que dia da semana é hoje? ").lower().strip()
FimDaSemana = ("sabado", "domingo")

if data in FimDaSemana:
    print("Bom fim de semana")
else:
    print("Boa semana")