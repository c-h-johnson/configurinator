from configurinator.config import bash
from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import is_exe


def run():
    if is_exe('starship'):
        with ConfigEditor(bash.bashrc) as cfg_edit:
            cfg_edit.add('eval "$(starship init bash)"', under='# prompt')

if __name__ == '__main__':
    run()
