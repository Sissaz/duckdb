## Pipeline for Data Processing and Storage

<div align="center">
<img width="55%" src="https://github.com/Sissaz/duckdb/blob/master/imagens/ETL.png?raw=true" /></a>
</div>

This project represents a comprehensive pipeline for processing and storing data, in this case, transportation data. This pipeline is designed to handle various tasks including downloading data from Google Drive, converting files to the appropriate encoding and date format, processing CSV files, and finally storing the processed data in a PostgreSQL database. Additionally, the code utilizes DuckDB for efficient data manipulation and transformation. This pipeline is particularly useful for managing large datasets in a structured and automated manner, ensuring data integrity and consistency throughout the process.

<div align="center">
<img width="50%" src="https://github.com/Sissaz/duckdb/blob/master/imagens/Fluxograma.png?raw=true" /></a>
</div>

#### Why use DuckDB?

- **Efficient Data Processing**: DuckDB is known for its high performance in data processing, especially with large datasets. It can handle complex queries and transformations efficiently, making it suitable for the data transformation step in the pipeline.

- **In-Memory Computation**: DuckDB operates primarily in memory, which allows for faster data manipulation and querying. This is particularly beneficial when dealing with multiple transformations and calculations on the dataset.

- **Compatibility with Pandas**: DuckDB integrates well with Pandas DataFrames, which are commonly used for data manipulation in Python. This allows for a seamless transition between reading data, processing it with DuckDB, and then storing it in a database.

- **Simplicity and Ease of Use**: DuckDB does not require a separate server or installation, making it easy to integrate into the existing pipeline. Its SQL-based interface is also straightforward for those familiar with SQL.

- **Cost-Effective**: DuckDB is an open-source database, which makes it a cost-effective solution for data processing and analysis.


##### [This code was developed with the assistance of a workshop conducted by Luciano Galvão Filho](https://www.youtube.com/live/eXXImkz-vMs?feature=shared): Thanks!


<div align="center">
<img width="100%" src="https://github.com/Sissaz/duckdb/blob/master/imagens/base_viagens.png?raw=true" /></a>
</div>


<div align="center">
<img width="100%" src="https://github.com/Sissaz/duckdb/blob/master/imagens/Render.png?raw=true" /></a>
</div>