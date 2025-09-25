from rich.console import Console
from rich.table import Table
from Model.fila.fila import Fila


class SJF:

    def __init__(self, processos=None):
        """
        Inicializa o escalonador SJF.

        :param processos: Lista de processos (opcional). Pode ser fornecida na criação da instância.
        """
        self.console = Console()
        self.fila_processos = Fila()
        self.processos = processos if processos is not None else []

    def escalonar(self, processos=None):
        """
        Executa o escalonamento SJF.

        :param processos: Lista de processos a escalonar. Se não fornecida, usa a lista da instância.
        :return: Lista de resultados contendo tempos de execução de cada processo.
        """
        if processos is None:
            processos = self.processos

        tempo_atual = 0
        resultados = []
        processos_restantes = processos.copy()

        while processos_restantes or len(self.fila_processos) > 0:
            # Adiciona processos que chegaram à fila
            for p in processos_restantes[:]:
                if p.get_tempo_chegada() <= tempo_atual:
                    self.fila_processos.push(p)
                    processos_restantes.remove(p)

            if len(self.fila_processos) == 0:
                if processos_restantes:
                    # Nenhum processo disponível, avança para o próximo
                    proximo = min(processos_restantes, key=lambda p: p.get_tempo_chegada())
                    tempo_atual = proximo.get_tempo_chegada()
                    self.fila_processos.push(proximo)
                    processos_restantes.remove(proximo)
                else:
                    break

            # Ordena a fila pelo menor tempo de execução
            self.ordenar_fila_por_tempo_execucao()

            # Executa o processo da frente da fila
            processo_atual = self.fila_processos.pop().data
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
        """
        Ordena a lista de processos pelo tempo de execução (menor primeiro) usando bubble sort.
        """
        tamanho_lista = len(processos)
        for i in range(tamanho_lista):
            for j in range(i + 1, tamanho_lista):
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
