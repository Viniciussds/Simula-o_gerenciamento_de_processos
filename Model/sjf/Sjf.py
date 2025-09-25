from Model.fila.fila import Fila

class SJF:
    def __init__(self, processos=None):
        self.fila_processos = Fila()
        self.processos = processos if processos else []

    def escalonar(self, processos=None):
        if processos is None:
            processos = self.processos

        tempo_atual = 0
        resultados = []
        processos_restantes = processos.copy()

        while processos_restantes or len(self.fila_processos) > 0:
            for p in processos_restantes[:]:
                if p.get_tempo_chegada() <= tempo_atual:
                    self.fila_processos.push(p)
                    processos_restantes.remove(p)

            if len(self.fila_processos) == 0:
                if processos_restantes:
                    proximo = min(processos_restantes, key=lambda p: p.get_tempo_chegada())
                    tempo_atual = proximo.get_tempo_chegada()
                    self.fila_processos.push(proximo)
                    processos_restantes.remove(proximo)
                else:
                    break

            # Ordena por menor tempo de execução
            self.ordenar_fila_por_tempo_execucao()
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

        return resultados

    def ordenar_fila_por_tempo_execucao(self):
        if self.fila_processos.eVazia():
            return
        processos = []
        while len(self.fila_processos) > 0:
            processos.append(self.fila_processos.pop().data)
        processos.sort(key=lambda p: p.get_tempo_execucao())
        for p in processos:
            self.fila_processos.push(p)
