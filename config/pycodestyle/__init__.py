from utils.env import dotfile_path
from utils.config import ConfigEditor

config_path = dotfile_path('.config/pycodestyle')


def run():
    with ConfigEditor(config_path) as cfg_edit:
        section = '[pycodestyle]'
        # more sensible than the standard 79
        cfg_edit.add('max-line-length = 236', under=section)
