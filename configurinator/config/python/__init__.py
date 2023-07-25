from config.python import history
from utils.env import dotfile_path

pythonrc = dotfile_path('.pythonrc')

def run():
    history.run()
