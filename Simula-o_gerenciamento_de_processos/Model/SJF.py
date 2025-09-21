class SJF:
    
    def __init__(self):
        self.fila_processos = []
    
    def escalonar(self, processos):
        processos_ordenados = self.ordenar_por_tempo_execucao(processos)
        fila_processos = self.adicionar_fila_execucao(processos_ordenados)
        processos_na_fila = len(fila_processos)
        numero_processos_executados = 0
        tempo_atual = 0
        while numero_processos_executados < processos_na_fila :
            for processo in fila_processos: 
                print(f"executando processo: {processo.get_id()}, Tempo chegada: {processo.get_tempo_chegada()}, Tempo de Execução: {processo.get_tempo_execucao()}")
                print(f"Tempo {tempo_atual}: executando processo {processo.get_id()}")
                tempo_atual += processo.get_tempo_execucao()
                print(f"Tempo {tempo_atual}: P {processo.get_id()} Finalisado")
                numero_processos_executados+=1
                
            
    def adicionar_fila_execucao(self, processos_ordenados):
        for processo in processos_ordenados:
            self.fila_processos.append(processo)
        return self.fila_processos
    
    def ordenar_por_tempo_execucao(self, processos):
        tamanho_lista = len(processos)
        for i in range(tamanho_lista):
            for j in range(i+1, tamanho_lista):
                    if processos[i].get_tempo_execucao() > processos[j].get_tempo_execucao():
                        atual = processos[i]
                        processos[i] = processos[j]
                        processos[j] = atual
        print("Ordem de execução dos processos (SJF):")
        return processos
        

            
            
        
        