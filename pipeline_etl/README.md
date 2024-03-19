## 💾 |  Pipeline for Data Processing and Storage

 #### [First Installations](https://github.com/Sissaz/duckdb/blob/master/pipeline_etl/instru%C3%A7%C3%B5es.md): Commands for setting up a development environment
 #### [Python Code](https://github.com/Sissaz/duckdb/blob/master/pipeline_etl/pipeline_etl.py): ETL Pipeline Code 

 #### Code Explained:

- **Importing libraries**: Imports various useful libraries for data processing, database connection, file manipulation, and environment variables.

- **Loading environment variables**: Using load_dotenv(), it loads the environment variables from the .env file, which usually contains sensitive or environment-specific information, such as database credentials.

- **Database connection**: The function conectar_banco() creates a connection to the DuckDB database. If the database does not exist, it will be created.

- **Table initialization**: The function inicializar_tabela(con) creates a table called historico_arquivos in the DuckDB database, if it does not already exist.

- **File registration**: The function registrar_arquivo(con, nome_arquivo) inserts a new record into the historico_arquivos table with the file name and the current time.

- **Checking processed files**: The function arquivos_processados(con) returns a set with the names of all the files that have already been processed.

- **UTF-8 encoding check**: The function is_utf8(filename) checks if a file is encoded in UTF-8.

- **Converting files to UTF-8**: The function converter_arquivos_para_utf8(diretorio, max_linhas=5000) converts CSV files in the specified directory to UTF-8 encoding.

- **Date conversion**: The function convert_date(date_str) converts date strings to the format '%Y/%m/%d'.

- **Date conversion in a CSV file**: The function convert_dates_in_csv_strict(file_path) applies date conversion to all columns of a CSV file that contain the word "data".

- **Folder processing**: The function process_folder(folder_path) processes all CSV files in a folder, converting the dates.

- **Downloading a folder from Google Drive**: The function baixar_pasta_google_drive(url_pasta, diretorio_local) downloads a folder from Google Drive to a local directory.

- **Listing files and types**: The function listar_arquivos_e_tipos(diretorio) lists the files in a directory and identifies whether they are CSV, JSON, or Parquet.

- **Reading a file**: The function ler_arquivo(caminho_do_arquivo, tipo) reads a file according to its type and returns a DataFrame.

- **DataFrame transformation**: The function transformar(df) applies various transformations to a DataFrame, including creating new columns and filtering records.

- **Saving to PostgreSQL**: The function salvar_no_postgres(df, tabela) saves a DataFrame to PostgreSQL.

- **Processing pipeline**: The function pipeline() orchestrates the entire process of downloading, converting, reading, transforming, and saving the data.

- **Points of attention identified with DuckDB**: Date columns must be in ISO 8601 format and files must be encoded in UTF-8.