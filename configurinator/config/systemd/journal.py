from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import rm


def run():
    # delete any existing persistent log files
    rm('/var/log/journal/')

    with ConfigEditor('/etc/systemd/journald.conf') as cfg_edit:
        under = '[Journal]'
        cfg_edit.add('Storage=volatile', under=under)


if __name__ == '__main__':
    run()
