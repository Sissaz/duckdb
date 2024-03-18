import os
import gdown
import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm

# Carrega as variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
def conectar_banco():
    """Conecta ao banco de dados DuckDB; cria o banco se não existir."""
    return duckdb.connect(database='duckdb.db', read_only=False)

# Inicialização da tabela
def inicializar_tabela(con):
    """Cria a tabela se ela não existir."""
    con.execute("""
        CREATE TABLE IF NOT EXISTS historico_arquivos (
            nome_arquivo VARCHAR,
            horario_processamento TIMESTAMP
        )
    """)

# Registro de arquivo
def registrar_arquivo(con, nome_arquivo):
    """Registra um novo arquivo no banco de dados com o horário atual."""
    con.execute("""
        INSERT INTO historico_arquivos (nome_arquivo, horario_processamento)
        VALUES (?, ?)
    """, (nome_arquivo, datetime.now()))

# Verificação de arquivos processados
def arquivos_processados(con):
    """Retorna um set com os nomes de todos os arquivos já processados."""
    return set(row[0] for row in con.execute("SELECT nome_arquivo FROM historico_arquivos").fetchall())

# Verificação de codificação UTF-8
def is_utf8(filename):
    try:
        with open(filename, encoding='utf-8', errors='strict') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

# Função para converter arquivos CSV para UTF-8
def converter_arquivos_para_utf8(diretorio, max_linhas=5000):
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

# Download de pasta do Google Drive
def baixar_pasta_google_drive(url_pasta, diretorio_local):
    os.makedirs(diretorio_local, exist_ok=True)
    gdown.download_folder(url_pasta, output=diretorio_local, quiet=False, use_cookies=False)

# Listagem de arquivos e tipos
def listar_arquivos_e_tipos(diretorio):
    """Lista arquivos e identifica se são CSV, JSON ou Parquet."""
    arquivos_e_tipos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv") or arquivo.endswith(".json") or arquivo.endswith(".parquet"):
            caminho_completo = os.path.join(diretorio, arquivo)
            tipo = arquivo.split(".")[-1]
            arquivos_e_tipos.append((caminho_completo, tipo))
    return arquivos_e_tipos

# Leitura de arquivo
def ler_arquivo(caminho_do_arquivo, tipo):
    """Lê o arquivo de acordo com seu tipo e retorna um DataFrame."""
    if tipo == 'csv':
        return duckdb.read_csv(caminho_do_arquivo, delimiter=';', quotechar='"', escapechar='\\', header=True)
    elif tipo == 'json':
        return pd.read_json(caminho_do_arquivo)
    elif tipo == 'parquet':
        return pd.read_parquet(caminho_do_arquivo)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {tipo}")

# Transformação de DataFrame
def transformar(df):
    # Executa a consulta SQL que inclui a nova coluna, operando sobre a tabela virtual
    df_transformado = duckdb.sql("""SELECT
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
                                valor_tarifa, 
                                valor_percentual_desconto, 
                                valor_aliquota_icms, 
                                valor_pedagio, 
                                valor_taxa_embarque, 
                                valor_total,     
                                CASE 
                                    WHEN in_passagem_cancelada = 'NÃO' THEN 'Não' 
                                    ELSE 'Sim' 
                                END AS cancelada,
                                TRIM(ponto_origem_viagem) as origem_viagem,
                                TRIM(ponto_destino_viagem) as destino_viagem,
                                CONCAT(TRIM(ponto_origem_viagem), ' - ', TRIM(ponto_destino_viagem)) AS origem_destino,
                                CASE 
                                    WHEN data_viagem = '2019-11-02' THEN 'Finados'
                                    WHEN data_viagem = '2019-11-15' THEN 'Proclamação da República'
                                    WHEN data_viagem = '2019-12-25' THEN 'Natal'
                                    WHEN data_viagem = '2020-01-01' THEN 'Confraternização Universal'
                                    ELSE 'Não é feriado'
                                END AS feriados,
                                SPLIT_PART(tipo_gratitude, ' - ', 1) AS tipo_gratuidade
                                FROM df
                                WHERE valor_total < 1000"""
                                 ).df()
    # Remove o registro da tabela virtual para limpeza
    print(df_transformado)
    return df_transformado

# Salvamento no PostgreSQL
def salvar_no_postgres(df, tabela):
    """Salva o DataFrame no PostgreSQL."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    df.to_sql(tabela, con=engine, if_exists='append', index=False)

# Pipeline de processamento
def pipeline():
    url_pasta = 'https://drive.google.com/drive/folders/1a03IPv2_lwqf5dh0650XQZNuyQ1RbpEH'
    diretorio_local = './arquivos_salvos'
    # Para fazer download dos arquivos, descomente o código abaixo
    baixar_pasta_google_drive(url_pasta, diretorio_local)
    converter_arquivos_para_utf8(diretorio_local)
    process_folder(diretorio_local)


    con = conectar_banco()
    inicializar_tabela(con)
    processados = arquivos_processados(con)
    arquivos_e_tipos = listar_arquivos_e_tipos(diretorio_local)

    logs = []
    for caminho_do_arquivo, tipo in arquivos_e_tipos:
        nome_arquivo = os.path.basename(caminho_do_arquivo)
        if nome_arquivo not in processados:
            df = ler_arquivo(caminho_do_arquivo, tipo)
            df_transformado = transformar(df)
            salvar_no_postgres(df_transformado, "base_viagens")
            registrar_arquivo(con, nome_arquivo)
            print(f"Arquivo {nome_arquivo} processado e salvo.")
            logs.append(f"Arquivo {nome_arquivo} processado e salvo.")

        else:
            print(f"Arquivo {nome_arquivo} já foi processado anteriormente.")
            logs.append(f"Arquivo {nome_arquivo} já foi processado anteriormente.")

    return logs
    

if __name__ == "__main__":
    pipeline()