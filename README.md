### No Powershell
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
- Altera a política de execução do PowerShell para permitir a execução de scripts.

- Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
- Baixa e executa o script de instalação do pyenv para Windows.

### No Bash
- code .
- Abre o Visual Studio Code na pasta atual.

### No VSCode
- curl -sSL https://install.python-poetry.org | python3 -
- Instala o Poetry usando o script oficial.

- poetry --version
- Exibe a versão do Poetry instalada.

- poetry config virtualenvs.in-project true
- Configura o Poetry para criar ambientes virtuais dentro do projeto.

- poetry install
- Instala as dependências do projeto com base no arquivo pyproject.toml.

- poetry init
- Inicia um novo projeto com Poetry, criando o arquivo pyproject.toml.

- poetry shell
- Ativa o ambiente virtual do projeto.

- poetry new base
- Cria um novo projeto Poetry chamado 'base'.

- pyenv local 3.12.1
- Define a versão local do Python para 3.12.1 usando pyenv.

- poetry env use 3.12.1
- Define a versão do Python para o ambiente virtual do Poetry.

- pyenv global 3.12.1
- Define a versão global do Python para 3.12.1 usando pyenv.

- poetry install --no-root
- Instala as dependências do projeto sem instalar o pacote raiz.

- poetry add streamlit
- Adiciona a biblioteca Streamlit como uma dependência do projeto.

- poetry add psycopg2-binary
- Adiciona a biblioteca psycopg2-binary como uma dependência do projeto.

- poetry add python-dotenv
- Adiciona a biblioteca python-dotenv como uma dependência do projeto.

- poetry add psycopg2
- Adiciona a biblioteca psycopg2 como uma dependência do projeto.

- poetry add sqlalchemy
- Adiciona a biblioteca SQLAlchemy como uma dependência do projeto.

- poetry add pandas
- Adiciona a biblioteca pandas como uma dependência do projeto.

- git add .
- Adiciona todas as mudanças ao índice do Git.

- git commit -m "update"
- Cria um commit com a mensagem "update".

- git push origin master
- Envia os commits para o repositório remoto na branch master.

### Alguns comandos não utilizados com poetry
- pip list
- Lista todas as bibliotecas instaladas.

- pip freeze
- Lista as versões das bibliotecas instaladas.

- pip freeze | grep -v "^-e" | xargs pip uninstall -y
- Desinstala todas as bibliotecas instaladas.

- python -m venv .venv
- Cria um ambiente virtual chamado .venv.

- source .venv/Scripts/activate
- Ativa o ambiente virtual .venv.

- deactivate
- Desativa o ambiente virtual atual.
