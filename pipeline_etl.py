# Rodando o arquivo no bash com: python pipeline_etl.py

import os
import gdown
import duckdb
import pandas as pd

from tqdm import tqdm
from sqlalchemy import create_engine
from dotenv import load_dotenv
from duckdb import DuckDBPyRelation
from pandas import DataFrame

def download_arquivos_gdrive(url_pasta, diretorio_local):
    print("Iniciando download dos arquivos do Google Drive...")
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet=False, use_cookies=False)
    print("Download concluído.")

# Função para listar arquivos CSV no diretorio especificado
def listar_arquivos_csv(diretorio):
    print("Listando arquivos CSV no diretório...")
    arquivos_csv = []
    todos_arquivos = os.listdir(diretorio)
    for arquivo in todos_arquivos:
        if arquivo.endswith(".csv"):
            caminho_completo = os.path.join(diretorio, arquivo)
            arquivos_csv.append(caminho_completo)
    print("Listagem concluída.")
    return arquivos_csv

def converter_arquivos_para_utf8(diretorio):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv') and not arquivo.endswith('_utf8.csv')]
    for arquivo in tqdm(arquivos_csv, desc="Convertendo arquivos para UTF-8"):  # Adiciona a barra de progresso
        nome_arquivo_sem_extensao = arquivo.split('.')[0]
        caminho_arquivo_origem = os.path.join(diretorio, arquivo)
        caminho_arquivo_destino = os.path.join(diretorio, f"{nome_arquivo_sem_extensao}_utf8.csv")
        # Se necessário, altere o encoding para o do arquivo csv utilizado. 
        # Algumas opções comuns incluem: 'UTF-8', 'ISO-8859-1' (latin1), 'windows-1252', 'UTF-16', 'ASCII', 'cp1251' (windows-1251), 'gbk'.
        df = pd.read_csv(caminho_arquivo_origem, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        df.to_csv(caminho_arquivo_destino, sep=';', index=False, encoding='utf-8')

# Função para ler um arquivo csv e retonar um dataframe duckdb
def ler_csv(caminho_arquivo):
    print("Iniciando leitura dos arquivos CSV...")
    for arquivo in caminho_arquivo:
        if arquivo.endswith("_utf8.csv"):  # Garante que estamos lendo apenas os arquivos convertidos
            dataframe = duckdb.read_csv(arquivo, sep=';', header=True, quotechar='"', date_format='%d-%m-%Y')
            # Para ver o DataFrame use o codigo abaixo
            #print(dataframe)      
    print("Leitura concluída.")
    return dataframe


def juntar_arquivos_csv(diretorio, arquivo_saida):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('_utf8.csv')]
    lista_dfs = []
    for arquivo in tqdm(arquivos_csv, desc="Juntando arquivos CSV"):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        lista_dfs.append(df)
    df_concatenado = pd.concat(lista_dfs, ignore_index=True)
    return df_concatenado  # Retorna o DataFrame concatenado


# Função para adicionar uma nova coluna:
def transformar(df: DuckDBPyRelation) -> DataFrame:
    # Executa a consulta SQL que inclui a nova coluna, operando sobre a tabela virtual
    df_transformado = duckdb.sql("SELECT *, CONCAT(codigo_viagem, '-', numero_bilhete, '-', numero_poltrona, '-', plataforma_embarque) AS codigo FROM df").df()
    # Remove o registro da tabela virtual para limpeza
    return df_transformado


if __name__ == "__main__":
    print("Iniciando o script...")
    url_pasta = 'https://drive.google.com/drive/folders/1a03IPv2_lwqf5dh0650XQZNuyQ1RbpEH'
    diretorio_local = './pasta_gdown'
    # download_arquivos_gdrive(url_pasta, diretorio_local)
    converter_arquivos_para_utf8(diretorio_local)
    arquivos = listar_arquivos_csv(diretorio_local)
    ler_csv(arquivos)
    df_concatenado = juntar_arquivos_csv(diretorio_local, 'arquivo_concatenado.csv')
    df_transformado = transformar(df_concatenado)  # Aplica a transformação ao DataFrame concatenado
    caminho_arquivo_saida = os.path.join(diretorio_local, 'arquivo_concatenado.csv')
    df_transformado.to_csv(caminho_arquivo_saida, sep=';', index=False, encoding='utf-8')  # Salva o DataFrame transformado no arquivo CSV
    print("Script concluído.")

