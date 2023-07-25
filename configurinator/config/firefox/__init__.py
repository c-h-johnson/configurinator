import configparser
import os
import platform

from config.firefox import prefs
from utils.env import dotfile_path

supported = True
try:
    if platform.system() == 'Linux':
        root = dotfile_path('.mozilla/firefox')
    elif platform.system() == 'Darwin':
        root = dotfile_path('Library/Application Support/Firefox')
    elif platform.system() == 'Windows':
        root = dotfile_path('AppData/Roaming/Mozilla/Firefox')
    else:
        supported = False

    if supported:
        installs = os.path.join(root, 'profiles.ini')
        _installs_cfg = configparser.ConfigParser()
        _installs_cfg.read(installs)

        default = os.path.join(root, _installs_cfg['Profile0']['Path'])
        print(f'found firefox user directory: {default}')
except KeyError:
    print('Error: need to setup firefox')
    supported = False


def run():
    if supported:
        prefs.run()
