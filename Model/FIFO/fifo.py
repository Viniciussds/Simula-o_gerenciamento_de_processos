from rich.console import Console
from rich.table import Table
from Model.fila.fila import Fila
from Model.Processo import Processo

class Fifo:
    def __init__(self, processos):
        self.console = Console()
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
        # Resetar processos para "Pronto"
        for p in self.todos_processos:
            p.set_estado_processo("Pronto")

        print("=== Início da Simulação FIFO ===\n")

        processos = sorted(self.todos_processos, key=lambda p: p.get_tempo_chegada())

        resultados = []

        while len(self.processos_finalizados) < len(processos):
            # Adiciona processos à fila que já chegaram
            for p in processos:
                if p.get_tempo_chegada() <= self.tempo_atual and p.get_estado_processo() == "Pronto":
                    self.fila_processos.push(p)
                    print(f"Tempo {self.tempo_atual}: Processo {p.get_id()} entrou na fila (Pronto)")

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

            resultados.append({
                "id": processo.get_id(),
                "chegada": processo.get_tempo_chegada(),
                "execucao": processo.get_tempo_execucao(),
                "inicio": tempo_inicio,
                "fim": self.tempo_atual,
                "wt": wt,
                "tt": tt
            })

            self.processos_finalizados.append(processo)

        self.exibir_resultados(resultados)
        print("=== Fim da Simulação ===")

    def exibir_resultados(self, resultados):
        table = Table(title="📌 Processos Escalonados (FIFO)")

        table.add_column("PID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Tempo Chegada", justify="center")
        table.add_column("Tempo Execução", justify="center")
        table.add_column("Tempo Início", justify="center", style="yellow")
        table.add_column("Tempo Fim", justify="center", style="green")
        table.add_column("WT", justify="center", style="red")
        table.add_column("TT", justify="center", style="magenta")

        soma_wt = 0
        soma_tt = 0

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
            soma_wt += r["wt"]
            soma_tt += r["tt"]

        # Média
        media_wt = soma_wt / len(resultados) if resultados else 0
        media_tt = soma_tt / len(resultados) if resultados else 0

        table.add_row(
            "Média",
            "-",
            "-",
            "-",
            "-",
            f"{media_wt:.2f}",
            f"{media_tt:.2f}"
        )

        self.console.print(table)
