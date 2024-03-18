import os
import pandas as pd
from tqdm import tqdm


def is_utf8(filename):
    try:
        with open(filename, encoding='utf-8', errors='strict') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

# Função para converter arquivos CSV para UTF-8
def converter_arquivos_para_utf8(diretorio, max_linhas=1000):
    arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.csv')]
    for arquivo in tqdm(arquivos_csv, desc="Verificando e convertendo arquivos para UTF-8"):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        if not is_utf8(caminho_arquivo):
            nome_arquivo_sem_extensao = arquivo.split('.')[0]
            caminho_arquivo_destino = os.path.join(diretorio, f"{nome_arquivo_sem_extensao}.csv")
            # Se necessário, altere o encoding para o do arquivo csv utilizado. 
            # Algumas opções comuns incluem: 'UTF-8', 'ISO-8859-1' (latin1), 'windows-1252', 'UTF-16', 'ASCII', 'cp1251' (windows-1251), 'gbk'.
            df = pd.read_csv(caminho_arquivo, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', nrows=max_linhas)
            df.to_csv(caminho_arquivo_destino, sep=';', index=False, encoding='utf-8')
        else:
            print(f" Arquivo {arquivo} já está em UTF-8.")

# Função para converter strings de datas
def convert_date(date_str):
    try:
        dt = pd.to_datetime(date_str, format='%d-%m-%Y', errors='raise')
        return dt.strftime('%Y/%m/%d')
    except:
        return date_str

# Função para converter as datas em um arquivo CSV específico
def convert_dates_in_csv_strict(file_path):
    df = pd.read_csv(file_path, delimiter=';', dtype=str)
    for column in df.columns:
        if 'data' in column.lower():
            df[column] = df[column].apply(convert_date)
    # Sobrescreve o arquivo original
    df.to_csv(file_path, index=False, sep=';')

# Função para processar todos os arquivos CSV em uma pasta
def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            convert_dates_in_csv_strict(file_path)
            print(f'Arquivo {file_name} processado com sucesso.')

# Caminho da pasta que contém os arquivos CSV
folder_path = './pasta_gdown2'
converter_arquivos_para_utf8(folder_path)
process_folder(folder_path)
