import json

def Ler_json(caminho_arquivo):
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        processos = json.load(f)

        print(processos)
    return processos
