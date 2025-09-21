from Model.Processo import Processo
from Model.SJF import SJF

lista_processos = [
    Processo(1, 0, 8),
    Processo(2, 1, 4),
    Processo(3, 2, 9),
]
algoritmo = SJF()
algoritmo.escalonar(lista_processos)