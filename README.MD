##  Simulação de Escalonamento de Processos

Este projeto implementa uma **simulação gráfica** dos algoritmos de escalonamento **FIFO** e **SJF** usando **Python** e **Tkinter**.  
A aplicação permite inserir processos, executar a simulação e visualizar de forma **animada** a execução de cada processo.

---

## Pré-requisitos

- **Python 3.10+** (recomendado Python 3.13).  
- Não é necessário instalar pacotes adicionais: o **Tkinter** já vem incluído no Python.

---

## Como executar

1. Clone ou baixe este projeto.  
2. Abra o terminal/cmd e vá até a pasta do projeto:  

   ```bash
   cd SIMULA-O_GERENCIAMENTO_DE_PROCESSOS

   ```
3. Execute o arquivo principal:  

   ```bash
   python main.py
   ```

---

##  Como usar a interface


1. Na tela principal escolha um algoritmo de escalonamento:
   - **Executar FIFO** → Escalonamento *First In, First Out*.  
   - **Executar SJF** → Escalonamento *Shortest Job First*.  

2. Durante a simulação:
   - A **fila de prontos** é atualizada dinamicamente.  
   - O processo em execução aparece como uma **barra de progresso animada**.  
   - Ao final, é exibida uma **tabela de resultados**.

---

##  Resultados exibidos

Cada processo terá calculado:  

- **Tempo de chegada**  
- **Tempo de execução**  
- **Tempo de início**  
- **Tempo de término**  
- **Tempo de espera (WT)**  
- **Turnaround Time (TT)**  
- **Média do tempo de espera (WT)**  
- **Média do Turnaround Time (TT)**  

---

##  Cenário de testes

Foram utilizados os processos fornecidos no enunciado:

P1: AT = 2,  PT = 15
P2: AT = 4,  PT = 6
P3: AT = 6,  PT = 11
P4: AT = 9,  PT = 8
P5: AT = 11, PT = 7

Também foram testados outros valores para AT e PT, inclusive iguais. O programa executou sem falhas.
