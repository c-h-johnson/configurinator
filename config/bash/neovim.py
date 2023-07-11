from common import group_exe
from config import bash
from utils.config import ConfigEditor
from utils.env import dotfile_path, is_exe, rm


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# reduce disk writes'

        if is_exe('nvim'):
            cfg_edit.add(f"alias nvim='{group_exe.editors['nvim'].command}'", under=under)

            rm(dotfile_path('.local/share/nvim/shada'))


if __name__ == '__main__':
    run()
