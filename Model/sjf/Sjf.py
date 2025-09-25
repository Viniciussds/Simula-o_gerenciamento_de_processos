from Model.fila.fila import Fila
from Model.Processo import Processo

class SJF:
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
        print("=== Início da Simulação SJF ===\n")

        for p in self.todos_processos:
            p.set_estado_processo("Pronto")

        while len(self.processos_finalizados) < len(self.todos_processos):
            for p in self.todos_processos:
                if p.get_tempo_chegada() <= self.tempo_atual and p.get_estado_processo() == "Pronto":
                    self.fila_processos.push(p)
                    p.set_estado_processo("NaFila")
                    print(f"Tempo {self.tempo_atual}: Processo {p.get_id()} entrou na fila (Pronto)")

            # Ordena fila pelo menor tempo de execução
            self.ordenar_fila_por_tempo_execucao()
            
            # Mostrar fila
            self.mostrar_fila()

            if self.fila_processos.eVazia():
                self.tempo_atual += 1
                continue

            # Executa próximo processo
            no = self.fila_processos.pop()
            processo = no.data
            processo.set_estado_processo("Executando")
            print(f"\nTempo {self.tempo_atual}: Processo {processo.get_id()} iniciou execução")
            self.mostrar_fila()

            # Calcula WT e TT
            tempo_inicio = max(self.tempo_atual, processo.get_tempo_chegada())
            wt = tempo_inicio - processo.get_tempo_chegada()
            self.tempo_atual = tempo_inicio + processo.get_tempo_execucao()
            tt = self.tempo_atual - processo.get_tempo_chegada()

            processo.set_estado_processo("Finalizado")
            print(f"Tempo {self.tempo_atual}: Processo {processo.get_id()} finalizado")
            print(f"WT: {wt} | TT: {tt}\n")

            self.processos_finalizados.append(processo)

        print("=== Fim da Simulação ===")

    def ordenar_fila_por_tempo_execucao(self):
        if self.fila_processos.eVazia():
            return
        processos = []
        while len(self.fila_processos) > 0:
            processos.append(self.fila_processos.pop().data)
        # Ordena pelo menor tempo de execução
        processos.sort(key=lambda p: p.get_tempo_execucao())
        # Reinsere na fila
        for p in processos:
            self.fila_processos.push(p)
