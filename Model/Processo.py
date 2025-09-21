class Processo:
    def __init__(self, id, tempo_chegada, tempo_execucao):
        self.id = id
        self.tempo_chegda = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.estado_processo = "Pronto"

    def get_estado_processo(self):
        return self.estado_processo

    def set_estado_processo(self, estado):
        self.estado_processo = estado

    def get_id(self):
        return self.id

    def get_tempo_chegada(self):
        return self.tempo_chegda

    def get_tempo_execucao(self):
        return self.tempo_execucao

    def set_id(self, id):
        self.id = id

    def set_tempo_execucao(self, tempo_execucao):
        self.tempo_execucao = tempo_execucao

    def set_tempo_chegada(self, tempo_chegada):
        self.tempo_chegda = tempo_chegada
