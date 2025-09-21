from Model.fila.fila import Fila
from Model.Processo import Processo


class Fifo:
    def __init__(self, processos):
        self.todos_processos = processos
        self.fila_processos = Fila()
        self.tempo_atual = 0
        self.processos_finalizados = []

    def mostrar_fila(self):
        fila_atual = []
        no = self.fila_processos.inicio
        while no:
            fila_atual.append(no.data.get_id())
            no = no.get_proximo()
        print(f"Fila atual: {fila_atual}")

    def escalonar(self):
        print("=== Início da Simulação FIFO ===\n")

        processos = sorted(self.todos_processos, key=lambda p: p.get_tempo_chegada())
        while len(self.processos_finalizados) < len(processos):
            # Adiciona processos à fila que já chegaram
            for p in processos:
                if p.get_tempo_chegada() <= self.tempo_atual and p.get_estado_processo() == "Pronto":
                    self.fila_processos.push(p)
                    print(f"Tempo {self.tempo_atual}: Processo {p.get_id()} entrou na fila (Pronto)")

            # Mostrar fila
            self.mostrar_fila()

            if self.fila_processos.eVazia():
                self.tempo_atual += 1  # Se não há processos prontos, avança o tempo
                continue

            # Executa próximo processo
            no = self.fila_processos.pop()
            processo = no.data
            processo.set_estado_processo("Executando")
            print(f"\nTempo {self.tempo_atual}: Processo {processo.get_id()} iniciou execução")
            self.mostrar_fila()

            # Calcula WT e TT
            tempo_inicio = self.tempo_atual
            wt = tempo_inicio - processo.get_tempo_chegada()
            self.tempo_atual += processo.get_tempo_execucao()
            tt = self.tempo_atual - processo.get_tempo_chegada()

            processo.set_estado_processo("Finalizado")
            print(f"Tempo {self.tempo_atual}: Processo {processo.get_id()} finalizado")
            print(f"WT: {wt} | TT: {tt}\n")

            self.processos_finalizados.append(processo)

        print("=== Fim da Simulação ===")
