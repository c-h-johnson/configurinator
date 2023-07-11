from config import python
from utils.config import ConfigEditor

def run():
    with ConfigEditor(python.pythonrc) as cfg_edit:
        cfg_edit.add('import readline\nreadline.write_history_file = lambda *args: None', under='# Disable writing interactive commands to storage (https://unix.stackexchange.com/a/297834)')

if __name__ == '__main__':
    run()
