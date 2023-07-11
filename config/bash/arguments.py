from config import bash
from utils.config import ConfigEditor
from utils.env import is_exe

def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# confirm before overwriting something'
        cfg_edit.add("alias rm='rm -i'", under=under)
        cfg_edit.add("alias cp='cp -i'", under=under)
        cfg_edit.add("alias mv='mv -i'", under=under)

        under = '# human-readable sizes'
        cfg_edit.add("alias df='df -h'", under=under)
        if is_exe('free'):
            cfg_edit.add("alias free='free -h'", under=under)

if __name__ == '__main__':
    run()
