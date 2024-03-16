### No Powershell
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
- Altera a política de execução do PowerShell para permitir a execução de scripts.
<br>

- Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
- Baixa e executa o script de instalação do pyenv para Windows.
<br>

### No Bash
- code .
- Abre o Visual Studio Code na pasta atual.
<br>

### No VSCode
- curl -sSL https://install.python-poetry.org | python3 -
- Instala o Poetry usando o script oficial.
<br>

- poetry --version
- Exibe a versão do Poetry instalada.
<br>

- poetry config virtualenvs.in-project true
- Configura o Poetry para criar ambientes virtuais dentro do projeto.
<br>

- poetry install
- Instala as dependências do projeto com base no arquivo pyproject.toml.
<br>

- poetry init
- Inicia um novo projeto com Poetry, criando o arquivo pyproject.toml.
<br>

- poetry shell
- Ativa o ambiente virtual do projeto.
<br>

- poetry new base
- Cria um novo projeto Poetry chamado 'base'.
<br>

- pyenv local 3.12.1
- Define a versão local do Python para 3.12.1 usando pyenv.
<br>

- poetry env use 3.12.1
- Define a versão do Python para o ambiente virtual do Poetry.
<br>

- pyenv global 3.12.1
- Define a versão global do Python para 3.12.1 usando pyenv.
<br>

- poetry install --no-root
- Instala as dependências do projeto sem instalar o pacote raiz.
<br>

- poetry add streamlit
- Adiciona a biblioteca Streamlit como uma dependência do projeto.
<br>

- poetry add gdown
- Adiciona a biblioteca gdown como uma dependência do projeto.
<br>

- poetry add psycopg2-binary
- Adiciona a biblioteca psycopg2-binary como uma dependência do projeto.
<br>

- poetry add python-dotenv
- Adiciona a biblioteca python-dotenv como uma dependência do projeto.
<br>

- poetry add psycopg2
- Adiciona a biblioteca psycopg2 como uma dependência do projeto.
<br>

- poetry add sqlalchemy
- Adiciona a biblioteca SQLAlchemy como uma dependência do projeto.
<br>

- poetry add pandas
- Adiciona a biblioteca pandas como uma dependência do projeto.
<br>

- git add .
- Adiciona todas as mudanças ao índice do Git.
<br>

- git commit -m "update"
- Cria um commit com a mensagem "update".
<br>

- git push origin master
- Envia os commits para o repositório remoto na branch master.
<br>

### Alguns comandos não utilizados com poetry
- pip list
- Lista todas as bibliotecas instaladas.
<br>

- pip freeze
- Lista as versões das bibliotecas instaladas.
<br>

- pip freeze | grep -v "^-e" | xargs pip uninstall -y
- Desinstala todas as bibliotecas instaladas.
<br>

- python -m venv .venv
- Cria um ambiente virtual chamado .venv.
<br>

- source .venv/Scripts/activate
- Ativa o ambiente virtual .venv.
<br>

- deactivate
- Desativa o ambiente virtual atual.
