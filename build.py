from py2exe import freeze
from pathlib import Path
import shutil

curdir = Path(__file__).parent
devops_dir = '.devops'
build_path = curdir.joinpath(devops_dir).joinpath("build").__str__()

freeze(
    windows=['main.py'],
    options={'dist_dir': build_path}
)
shutil.copy('installer.ps1', build_path)

