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

# Conecta ao banco de dados DuckDB
con = duckdb.connect(database='duckdb.db', read_only=False)

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

def is_utf8(filename):
    try:
        with open(filename, encoding='utf-8', errors='strict') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


# Função para converter arquivos CSV para UTF-8
def converter_arquivos_para_utf8(diretorio, max_linhas=8000):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv')]
    for arquivo in tqdm(arquivos_csv, desc="Verificando e convertendo arquivos para UTF-8"):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        if not is_utf8(caminho_arquivo):
            nome_arquivo_sem_extensao = arquivo.split('.')[0]
            caminho_arquivo_destino = os.path.join(diretorio, f"{nome_arquivo_sem_extensao}_utf8.csv")
            # Se necessário, altere o encoding para o do arquivo csv utilizado. 
            # Algumas opções comuns incluem: 'UTF-8', 'ISO-8859-1' (latin1), 'windows-1252', 'UTF-16', 'ASCII', 'cp1251' (windows-1251), 'gbk'.
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', nrows=max_linhas)
            df.to_csv(caminho_arquivo_destino, sep=';', index=False, encoding='utf-8')
        else:
            print(f" Arquivo {arquivo} já está em UTF-8.")


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
            CONCAT(codigo_viagem, '-', numero_bilhete, '-', numero_poltrona, '-', plataforma_embarque) AS codigo,
            CAST(codigo_viagem AS VARCHAR) AS codigo_viagem,
            CAST(cnpj AS VARCHAR) AS cnpj,
            CAST(numero_bilhete AS VARCHAR) AS numero_bilhete,                  
            CAST(categoria_transporte AS VARCHAR) AS categoria_transporte,
            CAST(nu_linha AS VARCHAR) AS nu_linha,
            CAST(tipo_servico AS VARCHAR) AS tipo_servico,              
            CAST(tipo_viagem AS VARCHAR) AS tipo_viagem,
            CAST(numero_poltrona AS VARCHAR) AS numero_poltrona,
            CAST(plataforma_embarque AS VARCHAR) AS plataforma_embarque,
            CAST(plataforma_embarque AS VARCHAR) AS origem_emissao,
            REPLACE(CAST(valor_tarifa AS VARCHAR), '.', ',') AS valor_tarifa, 
            REPLACE(CAST(valor_percentual_desconto AS VARCHAR), '.', ',') AS valor_percentual_desconto, 
            REPLACE(CAST(valor_aliquota_icms AS VARCHAR), '.', ',') AS valor_aliquota_icms, 
            REPLACE(CAST(valor_pedagio AS VARCHAR), '.', ',') AS valor_pedagio, 
            REPLACE(CAST(valor_taxa_embarque AS VARCHAR), '.', ',') AS valor_taxa_embarque, 
            REPLACE(CAST(valor_total AS VARCHAR), '.', ',') AS valor_total,                              
            TRIM(ponto_origem_viagem) as origem_viagem,
            TRIM(ponto_destino_viagem) as destino_viagem,
            CONCAT(TRIM(ponto_origem_viagem), ' - ', TRIM(ponto_destino_viagem)) AS origem_destino,
            CASE 
                WHEN in_passagem_cancelada = 'NÃO' THEN 'Não' 
                ELSE 'Sim' 
            END AS cancelada,
            STRPTIME(CAST(data_emissao_bilhete AS VARCHAR), '%d-%m-%Y') AS data_emissao_bilhete,
            STRPTIME(CAST(data_viagem AS VARCHAR), '%d-%m-%Y') AS data_viagem,
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

# Função para salvar o DataFrame no DuckDB
def salvar_duckdb(df, tabela):
    con.execute(f"CREATE TABLE IF NOT EXISTS {tabela} AS SELECT * FROM df;")
    con.execute(f"INSERT INTO {tabela} SELECT * FROM df;")


# Script principal
def pipeline():

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

    salvar_duckdb(df_transformado, 'base_viagens')  # Salva o DataFrame transformado no DuckDB
    print("Base salva no DuckDB.")



if __name__ == "__main__":
    pipeline()