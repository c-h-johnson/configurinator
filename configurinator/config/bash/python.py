from config import bash
from utils.config import ConfigEditor
from utils.env import is_exe


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# python'

        if is_exe('python3') or is_exe('python'):
            # file executed on interactive startup
            cfg_edit.add('export PYTHONSTARTUP=~/.pythonrc', under=under)

if __name__ == '__main__':
    run()
