from Model.fila.fila import Fila
from Model.Processo import Processo
from rich.console import Console
from rich.table import Table

class Fifo:
    def __init__(self, processos):
        self.todos_processos = processos
        self.fila_processos = Fila()
        self.tempo_atual = 0
        self.processos_finalizados = []
        self.console = Console()

    def mostrar_fila(self):
        fila_atual = []
        no = self.fila_processos.inicio
        while no:
            fila_atual.append(no.data.get_id())
            no = no.get_proximo()
        print(f"Fila atual: {fila_atual}")

    def escalonar(self):
        print("=== Início da Simulação FIFO ===\n")
        resultados = []

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
                self.tempo_atual += 1
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

            # Armazena resultados para tabela
            resultados.append({
                "id": processo.get_id(),
                "chegada": processo.get_tempo_chegada(),
                "execucao": processo.get_tempo_execucao(),
                "inicio": tempo_inicio,
                "fim": self.tempo_atual,
                "wt": wt,
                "tt": tt
            })

        print("=== Fim da Simulação ===\n")
        self.exibir_resultados(resultados)

    def exibir_resultados(self, resultados):
        table = Table(title="📌 Processos Escalonados (FIFO)")

        table.add_column("PID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Tempo Chegada", justify="center")
        table.add_column("Tempo Execução", justify="center")
        table.add_column("Tempo Início", justify="center", style="yellow")
        table.add_column("Tempo Fim", justify="center", style="green")
        table.add_column("WT", justify="center", style="red")
        table.add_column("TT", justify="center", style="magenta")

        for r in resultados:
            table.add_row(
                str(r["id"]),
                str(r["chegada"]),
                str(r["execucao"]),
                str(r["inicio"]),
                str(r["fim"]),
                str(r["wt"]),
                str(r["tt"])
            )

        self.console.print(table)
