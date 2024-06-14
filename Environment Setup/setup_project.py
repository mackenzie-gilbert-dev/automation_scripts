import os
import subprocess
import sys
import re
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_folder_name(folder_name):
    pattern = r'^[\w\- ]+$'
    if re.match(pattern, folder_name):
        logging.info(f"'{folder_name}' is a valid folder name.")
    else:
        logging.error(f"'{folder_name}' is not a valid folder name. Folder names must only contain alphanumeric characters, hyphens, and spaces.")
        sys.exit(1)

def check_python3_installed():
    try:
        # Use sys.executable to get the path to the current Python interpreter
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Python interpreter is installed: {result.stdout.strip()}")
        else:
            logging.error("Python interpreter is not installed.")
            sys.exit(1)
    except FileNotFoundError:
        logging.error("Python interpreter is not installed.")
        sys.exit(1)

def get_yes_no_input(prompt, retry_limit=3):
    for _ in range(retry_limit):
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            logging.info("Invalid input. Please answer 'yes' or 'no'.")
    logging.error("Too many invalid inputs.")
    sys.exit(1)

def manage_folder(folder_name):
    if os.path.exists(folder_name):
        use_existing = get_yes_no_input(f"The folder '{folder_name}' already exists. Do you want to use this existing folder? (yes/no): ")
        if use_existing:
            logging.info(f"Using the existing folder: {folder_name}")
            return True
        else:
            logging.info("User chose not to use the existing folder.")
            return False
    else:
        try:
            os.makedirs(folder_name)
            logging.info(f"Folder '{folder_name}' created.")
            return True
        except OSError as e:
            logging.error(f"Failed to create the folder '{folder_name}': {e}")
            return False

def create_pipfile(folder_name):
    pipfile_content = "# [[source]]\n# url = \"https://pypi.org/simple\"\n# verify_ssl = true\n# name = \"pypi\"\n\n# [packages]\n# db-dtypes = \"*\"\n\n# [dev-packages]\n# pytest = \"*\"\n# mypy = \"*\"\n# pandas-stubs = \"*\"\n\n# [requires]\n# python_version = \"3.11\""
    pipfile_path = os.path.join(folder_name, "Pipfile")

    if check_and_overwrite_file(pipfile_path):
        with open(pipfile_path, "w") as pipfile:
            pipfile.write(pipfile_content)
        logging.info("Pipfile created.")
    else:
        logging.info("The existing Pipfile was not overwritten.")

def create_gitignore(folder_name):
    gitignore_path = os.path.join(folder_name, ".gitignore")
    gitignore_content = "# Byte-compiled / optimized / DLL files\n__pycache__/\n*.py[cod]\n*$py.class\n\n# C extensions\n*.so\n\n# Distribution / packaging\n.Python\nbuild/\ndist/\ndownloads/\neggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\npip-wheel-metadata/\nshare/python-wheels/\n*.egg-info/\n.installed.cfg\n*.egg\nMANIFEST\n\n# PyInstaller\n*.manifest\n*.spec\n\n# Installer logs\npip-log.txt\npip-delete-this-directory.txt\n\n# Unit test / coverage reports\nhtmlcov/\n.tox/\n.nox/\n.coverage\n.coverage.*\n.cache\nnosetests.xml\ncoverage.xml\n*.cover\n*.py,cover\n.hypothesis/\n.pytest_cache/\n\n# Translations\n*.mo\n*.pot\n\n# Django stuff:\n*.log\nlocal_settings.py\ndb.sqlite3\ndb.sqlite3-journal\n\n# Flask stuff:\ninstance/\n.webassets-cache\n\n# Scrapy stuff:\n.scrapy\n\n# Sphinx documentation\ndocs/_build/\n\n# PyBuilder\ntarget/\n\n# Jupyter Notebook\n.ipynb_checkpoints\n\n# IPython\nprofile_default/\nipython_config.py\n\n# pyenv\n.python-version\n\n# pipenv\n#Pipfile.lock\n\n# PEP 582; used by e.g. github.com/David-OConnor/pyflow\n__pypackages__/\n\n# Celery stuff\ncelerybeat-schedule\ncelerybeat.pid\n\n# SageMath parsed files\n*.sage.py\n\n# Environments\n.env\n.venv\nenv/\nvenv/\nENV/\nenv.bak/\nvenv.bak/\n\n# Spyder project settings\n.spyderproject\n.spyproject\n\n# Rope project settings\n.ropeproject\n\n# mkdocs documentation\n/site\n\n# mypy\n.mypy_cache/\n.dmypy.json\ndmypy.json\n\n# Pyre type checker\n.pyre/\n"

    if check_and_overwrite_file(gitignore_path):
        with open(gitignore_path, "w") as gitignore:
            gitignore.write(gitignore_content)
        logging.info(".gitignore file created.")

def check_and_overwrite_file(file_path):
    if os.path.exists(file_path):
        response = get_yes_no_input(f"A file at {file_path} already exists. Do you want to overwrite it? (yes/no): ")
        if response.lower() == 'yes' or response.lower() == 'y':
            return True
        else:
            logging.info(f"User chose not to overwrite the existing file: {file_path}")
            return False
    return True

def create_project_structure(folder_name):
    """
    Creates essential project directories: 'src' for source files and 'tests' for test files.
    """
    try:
        # Paths for the src and tests directories
        src_path = os.path.join(folder_name, 'src')
        tests_path = os.path.join(folder_name, 'tests')

        # Create src directory if it doesn't exist
        if not os.path.exists(src_path):
            os.makedirs(src_path)
            logging.info(f"Source directory created at: {src_path}")
        else:
            logging.info(f"Source directory already exists at: {src_path}")

        # Create tests directory if it doesn't exist
        if not os.path.exists(tests_path):
            os.makedirs(tests_path)
            logging.info(f"Tests directory created at: {tests_path}")
        else:
            logging.info(f"Tests directory already exists at: {tests_path}")

    except OSError as e:
        logging.error(f"Failed to create project directories in '{folder_name}': {e}")
        sys.exit(1)

def main():
    check_python3_installed()

    folder_name = input("Enter the name of your python project: ").strip()
    verify_folder_name(folder_name)

    if manage_folder(folder_name):
        logging.info(f"Setup will proceed using the folder: {folder_name}")

        create_pipfile(folder_name)
        create_gitignore(folder_name)
        create_project_structure(folder_name)  # Call the function to create src and tests directories

    else:
        logging.info("Setup was cancelled by the user.")

if __name__ == "__main__":
    main()