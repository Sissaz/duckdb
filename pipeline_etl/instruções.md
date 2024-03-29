## ⚙️ | First Installations
Commands for setting up a development environment: adjusting policies in PowerShell, installing pyenv, opening VSCode, using Poetry for dependency management and Python versions with pyenv, and Git commands for version control. Commands for pip and venv are mentioned but not used with Poetry.

<br>

### In PowerShell
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Changes the execution policy of PowerShell to allow the execution of scripts.

- Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; & "./install-pyenv-win.ps1"

Downloads and executes the pyenv installation script for Windows.
<br><br>

### In Bash
- code .
Opens Visual Studio Code in the current folder.
<br><br>

### In VSCode
- curl -sSL https://install.python-poetry.org | python3 -

Installs Poetry using the official script.

<br>
- poetry --version

Displays the installed version of Poetry.

<br>
- poetry config virtualenvs.in-project true

Configures Poetry to create virtual environments within the project.

<br>
- poetry install

Installs the project dependencies based on the pyproject.toml file.

<br>
- poetry init

Starts a new project with Poetry, creating the pyproject.toml file.

<br>
- poetry shell

Activates the project's virtual environment.

<br>
- poetry new base

Creates a new Poetry project named 'base'.

<br>
- pyenv local 3.12.1

Sets the local version of Python to 3.12.1 using pyenv.

<br>
- poetry env use 3.12.1

Sets the Python version for the Poetry virtual environment.

<br>
- pyenv global 3.12.1

Sets the global version of Python to 3.12.1 using pyenv.

<br>
- poetry install --no-root

Installs the project dependencies without installing the root package.

<br>
- poetry add streamlit

Adds the Streamlit library as a project dependency.

<br>
- poetry add gdown

Adds the gdown library as a project dependency.

<br>
- poetry add psycopg2-binary

Adds the psycopg2-binary library as a project dependency.

<br>
- poetry add python-dotenv

Adds the python-dotenv library as a project dependency.

<br>
- poetry add psycopg2

Adds the psycopg2 library as a project dependency.

<br>
- poetry add sqlalchemy

Adds the SQLAlchemy library as a project dependency.

<br>
- poetry add pandas

Adds the pandas library as a project dependency.

<br>
- poetry add chardet

Adds the chardet library as a project dependency.

<br>
- git add . or git add filename

Adds all changes to the Git index.

<br>
- git commit -m "update"

Creates a commit with the message "update".

<br>
- git push origin master

Pushes commits to the remote repository on the master branch.

<br>

### Some commands not used with poetry
- pip list

Lists all installed libraries.

<br>
- pip freeze

Lists the versions of the installed libraries.

<br>
- pip freeze | grep -v "^-e" | xargs pip uninstall -y

Uninstalls all installed libraries.

<br>
- python -m venv .venv

Creates a virtual environment called .venv.

<br>
- source .venv/Scripts/activate

Activates the .venv virtual environment.

<br>
- deactivate

Deactivates the current virtual environment.