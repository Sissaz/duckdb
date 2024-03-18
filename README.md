## Pipeline para Processamento e Armazenamento de Dados

- Importação de bibliotecas: Importa várias bibliotecas úteis para o processamento de dados, conexão com banco de dados, manipulação de arquivos e variáveis de ambiente.

- Carregamento de variáveis de ambiente: Usando load_dotenv(), carrega as variáveis de ambiente do arquivo .env, que geralmente contém informações sensíveis ou específicas do ambiente, como credenciais de banco de dados.

- Conexão com o banco de dados: A função conectar_banco() cria uma conexão com o banco de dados DuckDB. Se o banco de dados não existir, ele será criado.

- Inicialização da tabela: A função inicializar_tabela(con) cria uma tabela chamada historico_arquivos no banco de dados DuckDB, se ela ainda não existir.

- Registro de arquivo: A função registrar_arquivo(con, nome_arquivo) insere um novo registro na tabela historico_arquivos com o nome do arquivo e o horário atual.

- Verificação de arquivos processados: A função arquivos_processados(con) retorna um conjunto com os nomes de todos os arquivos que já foram processados.

- Verificação de codificação UTF-8: A função is_utf8(filename) verifica se um arquivo está codificado em UTF-8.

- Conversão de arquivos para UTF-8: A função converter_arquivos_para_utf8(diretorio, max_linhas=5000) converte arquivos CSV no diretório especificado para a codificação UTF-8.

- Conversão de datas: A função convert_date(date_str) converte strings de data para o formato '%Y/%m/%d'.

- Conversão de datas em um arquivo CSV: A função convert_dates_in_csv_strict(file_path) aplica a conversão de datas a todas as colunas de um arquivo CSV que contenham a palavra "data".

- Processamento de pasta: A função process_folder(folder_path) processa todos os arquivos CSV em uma pasta, convertendo as datas.

- Download de pasta do Google Drive: A função baixar_pasta_google_drive(url_pasta, diretorio_local) baixa uma pasta do Google Drive para um diretório local.

- Listagem de arquivos e tipos: A função listar_arquivos_e_tipos(diretorio) lista os arquivos em um diretório e identifica se são CSV, JSON ou Parquet.

- Leitura de arquivo: A função ler_arquivo(caminho_do_arquivo, tipo) lê um arquivo de acordo com seu tipo e retorna um DataFrame.

- Transformação de DataFrame: A função transformar(df) aplica várias transformações a um DataFrame, incluindo a criação de novas colunas e a filtragem de registros.

- Salvamento no PostgreSQL: A função salvar_no_postgres(df, tabela) salva um DataFrame no PostgreSQL.

- Pipeline de processamento: A função pipeline() orquestra todo o processo de download, conversão, leitura, transformação e salvamento dos dados.

-Pontos de atenção identificados com o DuckDB:
- As colunas de data devem estar no formato ISO 8601;
- Os arquivos devem estar codificados em UTF-8;
