from config import bash
from utils.config import ConfigEditor
from utils.env import is_exe

def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# python env'

        if is_exe('pytest'):
            cfg_edit.add("alias pytest='export PYTHONPATH=$PWD && pytest'", under=under)

        if is_exe('python3') or is_exe('python'):
            if is_exe('python3') and not is_exe('python'):
                cfg_edit.add("alias python='export PYTHONPATH=$PWD && python3'", under=under)
            else:
                cfg_edit.add("alias python='export PYTHONPATH=$PWD && python'", under=under)

            # file executed on interactive startup
            cfg_edit.add('export PYTHONSTARTUP=~/.pythonrc', under=under)

if __name__ == '__main__':
    run()
