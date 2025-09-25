from copy import deepcopy
from Model.FIFO.fifo import Fifo
from Model.Processo import Processo
from Model.sjf.Sjf import SJF

# Criando processos
p1 = Processo("P1", 2, 15)
p2 = Processo("P2", 4, 6)
p3 = Processo("P3", 6, 11)
p4 = Processo("P4", 9, 8)
p5 = Processo("P5", 11, 7)

lista_processo = [p1, p2, p3, p4, p5]

def menu():
    while True:
        print("\n===== MENU DE SIMULAÇÃO =====")
        print("1 - Executar FIFO")
        print("2 - Executar SJF")
        print("3 - Executar ambos")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\n\n===== Simulação FIFO =====\n")
            fifo = Fifo(deepcopy(lista_processo))
            fifo.escalonar()
        elif escolha == "2":
            print("\n\n===== Simulação SJF =====\n")
            sjf = SJF(deepcopy(lista_processo))
            sjf.escalonar()
        elif escolha == "3":
            print("\n\n===== Simulação FIFO =====\n")
            fifo = Fifo(deepcopy(lista_processo))
            fifo.escalonar()
            print("\n\n===== Simulação SJF =====\n")
            sjf = SJF(deepcopy(lista_processo))
            sjf.escalonar()
        elif escolha == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
