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

# ===== Testando FIFO =====
print("\n\n===== Simulação FIFO =====\n")
fifo = Fifo(lista_processo)
fifo.escalonar()

# ===== Testando SJF =====
print("\n\n===== Simulação SJF =====\n")
sjf = SJF(lista_processo)
resultados = sjf.escalonar()
