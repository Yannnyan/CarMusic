""" This module builds the project """
from pathlib import Path
import shutil
import os
from py2exe import freeze

CUR_DIR = Path(__file__).parent
DEVOPS_DIR = '.devops'
DEVOPS_PATH = CUR_DIR.joinpath(DEVOPS_DIR)
BUILD_PATH = str(DEVOPS_PATH.joinpath("build"))

if not DEVOPS_PATH.exists():
    os.mkdir(str(DEVOPS_PATH))

freeze(
    windows=['main.py'],
    options={'dist_dir': BUILD_PATH}
)
shutil.copy('installer.ps1', BUILD_PATH)
