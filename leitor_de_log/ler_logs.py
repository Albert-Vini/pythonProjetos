import os
import re
import itertools
from collections import namedtuple, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

def ler_linha(linha, dict):
    """le uma linha de log tirando o ip e status do acesso"""
    padrao = r"^(([0-9]{1,3}\.){3}[0-9]{1,3}).*?\" (\d{3})"
    leitura = re.search(padrao, linha)
    if leitura:
        ip = leitura.group(1)
        status = leitura.group(3)
        dict[ip].append(status)

def ler_aquivo(localAquivo):
    """Le um arquivo com base na função ler_linha"""
    try:
        with open(localAquivo,mode="r", encoding="utf-8") as arquivo:
            dados_ips = defaultdict(list)
            for linha in arquivo:
                ler_linha(linha, dados_ips)
            return dados_ips
    except FileNotFoundError:
        print("não foi possivel abrir o arquivo")

##########################################################################################################################

def ler_lote(arquivo, tamanho):
    """Salva uma quantidade definidas de linhas de um arquivo em lista"""
    return list(itertools.islice(arquivo, tamanho))

def processar_bloco(dados_linhas):
    """Analisa todas as linhas de um determinado array de linhas"""
    dict_linhas = defaultdict(list)
    for linha in dados_linhas:
        ler_linha(linha, dict_linhas)
    return dict_linhas

def ler_arquivo_paralelo(local_arquivo):
    """
    Le um arquivo de log em txt devolvendo um dict com ips e status de cada acesso(forma paralela pra muitos dados)
    """
    try:
        dict_final = defaultdict(list)
        with open(local_arquivo, "r") as arquivo:
            with ProcessPoolExecutor() as executor:
                processos = []
                blocoAtual = ler_lote(arquivo, 5000)
                while blocoAtual:
                    futuros_resultados = executor.submit(processar_bloco, blocoAtual)
                    processos.append(futuros_resultados)

                    blocoAtual = ler_lote(arquivo, 5000)
                for futuro in as_completed(processos):
                    dicionario_parcial = futuro.result()
                    for (ip,status_lista) in dicionario_parcial.items():
                        dict_final[ip].extend(status_lista)
        return dict_final
    except FileNotFoundError:
        print("não foi possivel encontrar o arquivo")

if __name__ == '__main__':
    print(ler_arquivo_paralelo("leitor_de_log/log.txt"))