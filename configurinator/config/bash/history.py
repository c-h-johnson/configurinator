from configurinator.config import bash
from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import dotfile_path, rm


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# reduce disk writes'
        cfg_edit.add('unset HISTFILE', under=under)
        cfg_edit.add('export LESSHISTFILE=/dev/null', under=under)

        rm(dotfile_path('.bash_history'))
        rm(dotfile_path('.lesshst'))


if __name__ == '__main__':
    run()
