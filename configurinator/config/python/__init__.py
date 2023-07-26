from configurinator.config.python import history
from configurinator.utils.env import dotfile_path

pythonrc = dotfile_path('.pythonrc')

def run():
    history.run()
