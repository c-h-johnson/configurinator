from configurinator.config import bash
from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import is_exe


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# alternatives'
        if is_exe('exa'):
            cfg_edit.add("alias ls='exa --long --all --header --git'", under=under)


if __name__ == '__main__':
    run()
