from Model.fila.fila import Fila

class Fifo:
    def __init__(self, processos):
        self.todos_processos = processos
        self.fila_processos = Fila()
        self.tempo_atual = 0
        self.processos_finalizados = []

    def escalonar(self):
        resultados = []
        processos = sorted(self.todos_processos, key=lambda p: p.get_tempo_chegada())

        while len(self.processos_finalizados) < len(processos):
            # Adiciona novos processos à fila apenas uma vez
            for p in processos:
                if (
                    p.get_tempo_chegada() <= self.tempo_atual 
                    and p.get_estado_processo() == "Pronto"
                ):
                    self.fila_processos.push(p)
                    p.set_estado_processo("NaFila")  # marca que já foi enfileirado

            if self.fila_processos.eVazia():
                self.tempo_atual += 1
                continue

            no = self.fila_processos.pop()
            processo = no.data

            processo.set_estado_processo("Executando")
            tempo_inicio = self.tempo_atual

            wt = tempo_inicio - processo.get_tempo_chegada()
            self.tempo_atual += processo.get_tempo_execucao()
            tt = self.tempo_atual - processo.get_tempo_chegada()

            processo.set_estado_processo("Finalizado")
            self.processos_finalizados.append(processo)

            resultados.append({
                "id": processo.get_id(),
                "chegada": processo.get_tempo_chegada(),
                "execucao": processo.get_tempo_execucao(),
                "inicio": tempo_inicio,
                "fim": self.tempo_atual,
                "wt": wt,
                "tt": tt
            })

        return resultados
