## Pipeline for Data Processing and Storage

This project represents a comprehensive pipeline for processing and storing data, in this case, transportation data. This pipeline is designed to handle various tasks including downloading data from Google Drive, converting files to the appropriate encoding and date format, processing CSV files, and finally storing the processed data in a PostgreSQL database. Additionally, the code utilizes DuckDB for efficient data manipulation and transformation. This pipeline is particularly useful for managing large datasets in a structured and automated manner, ensuring data integrity and consistency throughout the process.

#### Why use DuckDB?


- **Efficient Data Processing**: DuckDB is known for its high performance in data processing, especially with large datasets. It can handle complex queries and transformations efficiently, making it suitable for the data transformation step in the pipeline.

- **In-Memory Computation**: DuckDB operates primarily in memory, which allows for faster data manipulation and querying. This is particularly beneficial when dealing with multiple transformations and calculations on the dataset.

- **Compatibility with Pandas**: DuckDB integrates well with Pandas DataFrames, which are commonly used for data manipulation in Python. This allows for a seamless transition between reading data, processing it with DuckDB, and then storing it in a database.

- **Simplicity and Ease of Use**: DuckDB does not require a separate server or installation, making it easy to integrate into the existing pipeline. Its SQL-based interface is also straightforward for those familiar with SQL.

- **Cost-Effective**: DuckDB is an open-source database, which makes it a cost-effective solution for data processing and analysis.


#### Code Explained

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