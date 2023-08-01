from configurinator.common import group_exe
from configurinator.config import bash
from configurinator.utils.config import ConfigEditor
from configurinator.utils.ui import select_exe


def run(store):
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# editor'

        editor_cmd = store.use('bash.env.editor', lambda: select_exe(group_exe.EDITOR.values()))
        cfg_edit.add(f"export EDITOR='{editor_cmd}'", under=under)


if __name__ == '__main__':
    run()
