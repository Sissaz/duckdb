# Rodando o arquivo no bash com: python pipeline_etl.py

import os
import gdown
import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def download_arquivos_gdrive(url_pasta, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet= False, use_cookies=False)

# Função para listar arquivos CSV no diretorio especificado
def listar_arquivos_csv(diretorio):
    arquivos_csv = []
    todos_arquivos = os.listdir(diretorio)
    for arquivo in todos_arquivos:
            if arquivo.endswith(".csv"):
                caminho_completo = os.path.join(diretorio, arquivo)
                arquivos_csv.append(caminho_completo)
    return arquivos_csv

def converter_arquivos_para_utf8(diretorio):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv') and not arquivo.endswith('_utf8.csv')]
    for arquivo in arquivos_csv:
        nome_arquivo_sem_extensao = arquivo.split('.')[0]
        caminho_arquivo_origem = os.path.join(diretorio, arquivo)
        caminho_arquivo_destino = os.path.join(diretorio, f"{nome_arquivo_sem_extensao}_utf8.csv")
        df = pd.read_csv(caminho_arquivo_origem, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        df.to_csv(caminho_arquivo_destino, sep=';', index=False, encoding='utf-8')
        print(f"Arquivo convertido: {caminho_arquivo_destino}")


# Função para ler um arquivo csv e retonar um dataframe duckdb
def ler_csv(caminho_arquivo):
    for arquivo in caminho_arquivo:
        if arquivo.endswith("_utf8.csv"):  # Garante que estamos lendo apenas os arquivos convertidos
            dataframe = duckdb.read_csv(arquivo, sep=';', header=True, quotechar='"', date_format='%d-%m-%Y')
            print(dataframe)
            print(type(dataframe))
    return dataframe

if __name__ == "__main__":
    url_pasta = 'https://drive.google.com/drive/folders/1a03IPv2_lwqf5dh0650XQZNuyQ1RbpEH'
    diretorio_local = './pasta_gdown'
    # download_arquivos_gdrive(url_pasta, diretorio_local)
    converter_arquivos_para_utf8(diretorio_local)
    arquivos = listar_arquivos_csv(diretorio_local)
    ler_csv(arquivos)