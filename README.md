# duckdb
Consulta apenas
- No powershell 
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser (Instalando pyenv)
- Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1" (Instalando pyenv)

- No bash
- poetry new base // criar nova pasta do projeto pelo poetry
- pyenv local 3.12.1 // versão python
- poetry env use 3.12.1 // versão python
- poetry add pandas // instalar biblioteca
- code . // abrir o vscode na pasta que o bash está
- poetry shell


- Configurações no Bash
- pyenv install 3.12.1
- pyenv global 3.12.1
- pyenv --version
- pip install django
- pip install pandas
- pip install streamlit
- pip list // listagem de bibliotecas
- pip freeze //  versão das bibliotecas
- pip freeze | grep -v "^-e" | xargs pip uninstall -y // desinstalar todas bibliotecas
- python -m venv .venv // criar o ambiente virtual
- source .venv/Scripts/activate // ativar o ambiente virtual
- deactivate // sair do ambiente vitual
- pip installl poetry // ambiente virtual
- poetry config virtualenvs.in-project true
- git add . // update no github
- git commit -m "update" // update no github
- git push origin master // update no github
