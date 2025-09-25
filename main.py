from copy import deepcopy
from Model.Processo import Processo
from Model.FIFO.fifo import Fifo
from Model.sjf.Sjf import SJF

def criar_processos():
    p1 = Processo("P1", 2, 15)
    p2 = Processo("P2", 4, 6)
    p3 = Processo("P3", 6, 11)
    p4 = Processo("P4", 9, 8)
    p5 = Processo("P5", 11, 7)
    return [p1, p2, p3, p4, p5]

def menu():
    while True:
        print("\n===== Simulador de Escalonamento =====")
        print("1 - Executar FIFO")
        print("2 - Executar SJF")
        print("3 - Executar Ambos (FIFO + SJF)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            lista_processo = criar_processos()
            print("\n===== Simulação FIFO =====\n")
            fifo = Fifo(deepcopy(lista_processo))
            fifo.escalonar()

        elif opcao == "2":
            lista_processo = criar_processos()
            print("\n===== Simulação SJF =====\n")
            sjf = SJF()
            sjf.escalonar(deepcopy(lista_processo))

        elif opcao == "3":
            lista_processo = criar_processos()
            print("\n===== Simulação FIFO =====\n")
            fifo = Fifo(deepcopy(lista_processo))
            fifo.escalonar()

            print("\n===== Simulação SJF =====\n")
            sjf = SJF()
            sjf.escalonar(deepcopy(lista_processo))

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Digite novamente.")

if __name__ == "__main__":
    menu()
