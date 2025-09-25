from rich.console import Console
from rich.table import Table
from Model.fila.fila import Fila

class SJF:

    def __init__(self):
        self.console = Console()
        self.fila_processos = Fila()

    def escalonar(self, processos):
        tempo_atual = 0
        resultados = []
        processos_restantes = processos.copy()

        while processos_restantes or len(self.fila_processos) > 0:

            # Adiciona processos à fila que já chegaram
            for p in processos_restantes[:]:  # iterando sobre uma cópia
                if p.get_tempo_chegada() <= tempo_atual:
                    self.fila_processos.push(p)
                    processos_restantes.remove(p)

            # Se a fila estiver vazia, avança para o próximo processo que chegar
            if len(self.fila_processos) == 0:
                if processos_restantes:
                    proximo = min(processos_restantes, key=lambda p: p.get_tempo_chegada())
                    tempo_atual = proximo.get_tempo_chegada()
                    self.fila_processos.push(proximo)
                    processos_restantes.remove(proximo)
                else:
                    break

            # Ordena a fila pelo menor tempo de execução
            self.ordenar_fila_por_tempo_execucao()

            # Executa o primeiro processo da fila
            processo_atual = self.fila_processos.pop().data

            # Calcula tempos
            inicio = max(tempo_atual, processo_atual.get_tempo_chegada())
            fim = inicio + processo_atual.get_tempo_execucao()
            wt = inicio - processo_atual.get_tempo_chegada()
            tt = fim - processo_atual.get_tempo_chegada()
            tempo_atual = fim

            resultados.append({
                "id": processo_atual.get_id(),
                "chegada": processo_atual.get_tempo_chegada(),
                "execucao": processo_atual.get_tempo_execucao(),
                "inicio": inicio,
                "fim": fim,
                "wt": wt,
                "tt": tt
            })

            print(f"Tempo {inicio}: executando P{processo_atual.get_id()}")
            print(f"Tempo {fim}: P{processo_atual.get_id()} finalizado (WT={wt}, TT={tt})\n")

        self.exibir_resultados(resultados)
        return resultados

    def ordenar_fila_por_tempo_execucao(self):
        if self.fila_processos.eVazia():
            return
        processos = []
        while len(self.fila_processos) > 0:
            processos.append(self.fila_processos.pop().data)

        processos_ordenados = self.ordenar_por_tempo_execucao(processos)

        for processo in processos_ordenados:
            self.fila_processos.push(processo)

    def ordenar_por_tempo_execucao(self, processos):
        tamanho_lista = len(processos)
        for i in range(tamanho_lista):
            for j in range(i+1, tamanho_lista):
                if processos[i].get_tempo_execucao() > processos[j].get_tempo_execucao():
                    processos[i], processos[j] = processos[j], processos[i]
        return processos

    def exibir_resultados(self, resultados):
        table = Table(title="📌 Processos Escalonados (SJF)")

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
