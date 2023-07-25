from common import group_exe
from config import bash
from utils.config import ConfigEditor
from utils.ui import select_exe


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# editor'

        editor_cmd = select_exe(group_exe.editors.values())
        cfg_edit.add(f"export EDITOR='{editor_cmd}'", under=under)


if __name__ == '__main__':
    run()
