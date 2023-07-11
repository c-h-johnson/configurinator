from config import bash
from utils.config import ConfigEditor


def run():
    with ConfigEditor(bash.profile_path) as cfg_edit:
        cfg_edit.add('[[ -f ~/.bashrc ]] && . ~/.bashrc')


if __name__ == '__main__':
    run()
