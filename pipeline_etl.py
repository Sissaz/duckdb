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

load_dotenv()

# Função para baixar arquivos do Google Drive para um diretório local
def download_arquivos_gdrive(url_pasta, diretorio_local):
    print("Iniciando download dos arquivos do Google Drive...")
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet=False, use_cookies=False)
    print("Download concluído.")


# Função para listar arquivos CSV em um diretório
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


# Função para converter arquivos CSV para UTF-8
def converter_arquivos_para_utf8(diretorio, max_linhas=8000):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv') and not arquivo.endswith('_utf8.csv')]
    for arquivo in tqdm(arquivos_csv, desc="Convertendo arquivos para UTF-8"):
        nome_arquivo_sem_extensao = arquivo.split('.')[0]
        caminho_arquivo_origem = os.path.join(diretorio, arquivo)
        caminho_arquivo_destino = os.path.join(diretorio, f"{nome_arquivo_sem_extensao}_utf8.csv")
        # Se necessário, altere o encoding para o do arquivo csv utilizado. 
        # Algumas opções comuns incluem: 'UTF-8', 'ISO-8859-1' (latin1), 'windows-1252', 'UTF-16', 'ASCII', 'cp1251' (windows-1251), 'gbk'.
        df = pd.read_csv(caminho_arquivo_origem, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', nrows=max_linhas)
        df.to_csv(caminho_arquivo_destino, sep=';', index=False, encoding='utf-8')


# Função para ler arquivos CSV e retornar um dataframe DuckDB
def ler_csv(caminho_arquivo):
    print("Iniciando leitura dos arquivos CSV...")
    for arquivo in caminho_arquivo:
        if arquivo.endswith("_utf8.csv"):  # Garante que estamos lendo apenas os arquivos convertidos
            dataframe = duckdb.read_csv(arquivo, sep=';', header=True, quotechar='"', date_format='%d-%m-%Y')
            # Para ver o DataFrame use o codigo abaixo
            #print(dataframe)      
    print("Leitura concluída.")
    return dataframe


# Função para juntar vários arquivos CSV em um único DataFrame
def juntar_arquivos_csv(diretorio, arquivo_saida, max_linhas=8000):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('_utf8.csv')]
    lista_dfs = []
    for arquivo in tqdm(arquivos_csv, desc="Juntando arquivos CSV"):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8', nrows=max_linhas)
        lista_dfs.append(df)
    df_concatenado = pd.concat(lista_dfs, ignore_index=True)
    return df_concatenado # Retorna o DataFrame concatenado


# Função para transformar um DataFrame DuckDB, adicionando uma nova coluna concatenada
def transformar(df: DuckDBPyRelation) -> DataFrame:
    # Executa a consulta SQL que inclui as novas colunas
    df_transformado = duckdb.sql("""
        SELECT 
            codigo_viagem, cnpj, numero_bilhete, data_emissao_bilhete, categoria_transporte, nu_linha,
            tipo_servico, data_viagem, hora_viagem, tipo_viagem, numero_poltrona, plataforma_embarque, origem_emissao,
            REPLACE(CAST(valor_tarifa AS VARCHAR), '.', ',') AS valor_tarifa, 
            REPLACE(CAST(valor_percentual_desconto AS VARCHAR), '.', ',') AS valor_percentual_desconto, 
            REPLACE(CAST(valor_aliquota_icms AS VARCHAR), '.', ',') AS valor_aliquota_icms, 
            REPLACE(CAST(valor_pedagio AS VARCHAR), '.', ',') AS valor_pedagio, 
            REPLACE(CAST(valor_taxa_embarque AS VARCHAR), '.', ',') AS valor_taxa_embarque, 
            REPLACE(CAST(valor_total AS VARCHAR), '.', ',') AS valor_total,                              
            CONCAT(codigo_viagem, '-', numero_bilhete, '-', numero_poltrona, '-', plataforma_embarque) AS codigo,
            CONCAT(TRIM(ponto_origem_viagem), ' - ', TRIM(ponto_destino_viagem)) AS origem_destino,
            TRIM(ponto_origem_viagem) as origem_viagem,
            TRIM(ponto_destino_viagem) as destino_viagem,
            CASE 
                WHEN in_passagem_cancelada = 'NÃO' THEN 'Não' 
                ELSE 'Sim' 
            END AS cancelada,
            SUBSTRING(data_viagem, 1, 5) AS dia_mes_viagem,  -- Extrai os 5 primeiros caracteres (DD-MM)
            SUBSTRING(data_viagem, 4, 7) AS mes_viagem, -- Extrai os últimos 7 caracteres (MM-YYYY)
            SPLIT_PART(tipo_gratitude, ' - ', 1) AS tipo_gratuidade, -- Extrai texto antes do delimitador " - "
            CASE 
                WHEN data_viagem = '02-11-2019' THEN 'Finados'
                WHEN data_viagem = '15-11-2019' THEN 'Proclamação da República'
                WHEN data_viagem = '25-12-2019' THEN 'Natal'
                WHEN data_viagem = '01-01-2020' THEN 'Confraternização Universal'
                ELSE 'Não é feriado'
            END AS feriados
        FROM df
        WHERE valor_total < 1000  -- Adiciona a cláusula WHERE para retirar os valores discrepantes das passagens
    """).df()
    return df_transformado


# Função para converter o Duckdb em Pandas e salar o DataFrame no PostgreSQL
def salvar_postgres(df_duckdb, tabela):
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    # Salvar o DataFrame no PostgreSQL
    df_duckdb.to_sql(tabela, con=engine, if_exists='append', index=False)


# Script principal
if __name__ == "__main__":
    print("Iniciando o script...")
    url_pasta = 'https://drive.google.com/drive/folders/xxxxxxxxxxxxxxxxx'
    diretorio_local = './pasta_gdown'
    # Para fazer download dos arquivos, descomente o código abaixo
    # download_arquivos_gdrive(url_pasta, diretorio_local)
    converter_arquivos_para_utf8(diretorio_local)
    arquivos = listar_arquivos_csv(diretorio_local)
    ler_csv(arquivos)
    df_concatenado = juntar_arquivos_csv(diretorio_local, 'base_viagens.csv')
    df_transformado = transformar(df_concatenado)  # Aplica a transformação ao DataFrame concatenado
    caminho_arquivo_saida = os.path.join(diretorio_local, 'base_viagens.csv')
    df_transformado.to_csv(caminho_arquivo_saida, sep=';', index=False, encoding='utf-8')  # Salva o DataFrame transformado no arquivo CSV
    print("Base salva localmente.")
    salvar_postgres(df_transformado, 'base_viagens')  # Salva o DataFrame transformado no PostgreSQL
    print("Base salva no PostgreSQL.")