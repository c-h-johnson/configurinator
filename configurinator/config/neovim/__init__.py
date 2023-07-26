import platform

from configurinator.config.neovim import init
from configurinator.utils.env import dotfile_path

supported = True
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    root = dotfile_path('.config/nvim')
elif platform.system() == 'Windows':
    root = dotfile_path('AppData/Local/nvim')
else:
    supported = False


def run():
    if supported:
        init.run()
