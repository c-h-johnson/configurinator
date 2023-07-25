from config.git import gitconfig
from utils.env import dotfile_path

gitconfig_path = dotfile_path('.gitconfig')


def run():
    gitconfig.run()
