""" This module builds the project """
from pathlib import Path
import shutil
from py2exe import freeze

CUR_DIR = Path(__file__).parent
DEVOPS_DIR = '.devops'
BUILD_PATH = str(CUR_DIR.joinpath(DEVOPS_DIR).joinpath("build"))

freeze(
    windows=['main.py'],
    options={'dist_dir': BUILD_PATH}
)
shutil.copy('installer.ps1', BUILD_PATH)
