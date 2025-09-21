from Model.FIFO.fifo import Fifo
from Model.Processo import Processo

# Criando processos
p1 = Processo("P1", 2, 15)
p2 = Processo("P2", 4, 6)
p3 = Processo("P3", 6, 11)
p4 = Processo("P4", 9, 8)
p5 = Processo("P5", 11, 7)

# Adicionando processos à fila
fifo = Fifo([p1, p2, p3, p4, p5])
fifo.fila_processos.push(p1)
fifo.fila_processos.push(p2)
fifo.fila_processos.push(p3)
fifo.fila_processos.push(p4)
fifo.fila_processos.push(p5)
# Executando a simulação
fifo.escalonar()
