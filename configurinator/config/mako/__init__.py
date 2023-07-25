from utils.config import ConfigEditor
from utils.env import dotfile_path

config_path = dotfile_path('.mako/config')

def run():
    with ConfigEditor(config_path) as cfg_edit:
        cfg_edit.add('anchor=bottom-right')
        cfg_edit.add('default-timeout=10000')
        cfg_edit.add('layer=overlay')
