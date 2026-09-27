import os
""" 
Lê o volume inicial de combustível, o volume consumido e a densidade do combustível em kg/L.
Calcula primeiro o volume restante e depois a respetiva massa
"""
def combustivel():
    combustivelI = float(input("Qual o volume inicial de combustivel?\n"))
    consumo = float(input("Qual foi o volume consumido?\n"))
    densidade = float(input("Qual é a densidade do combustivel?\n"))
    os.system("clear")

    sobraCombustivel = combustivelI-consumo
    print("Sobraram ", sobraCombustivel, "L de combustivel")
    pesoCombustivel = sobraCombustivel * densidade
    print("Que pesa aproximadamente ",pesoCombustivel)
    return 1

combustivel()
