# duckdb
Consulta apenas

- No powershell 
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser (Instalando pyenv)
- Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1" (Instalando pyenv)

Git: Versionamento do código
Pyenv: Versão do Python
Poetry: Ambiente Virtual

- No bash
- poetry init
- poetry shell // se sair do terminal do bash tem que ativar novamente o shell
- poetry new base // criar nova pasta do projeto pelo poetry (opcional caso já tiver criado)
- pyenv local 3.12.1 // versão python
- poetry env use 3.12.1 // versão python
- pyenv global 3.12.1
- poetry install
- poetry install --no-root
- poetry add streamlit
- poetry add psycopg2-binary
- poetry add python-dotenv
- poetry add psycopg2
- poetry add sqlalchemy
- poetry add pandas // instalar biblioteca
- code . // abrir o vscode na pasta que o bash está


- Outras configurações no Bash (não usando com poetry)
- pip list // listagem de bibliotecas
- pip freeze //  versão das bibliotecas
- pip freeze | grep -v "^-e" | xargs pip uninstall -y // desinstalar todas bibliotecas
- python -m venv .venv // criar o ambiente virtual
- source .venv/Scripts/activate // ativar o ambiente virtual
- deactivate // sair do ambiente vitual
- pip installl poetry // ambiente virtual
- poetry config virtualenvs.in-project true


- Commitar mudanças no github
- git add . // update no github
- git commit -m "update" // update no github
- git push origin master // update no github
xxxxxxxxxxxxxxxxxxxxxxxxxxx