from configurinator.config.git import gitconfig
from configurinator.utils.env import dotfile_path

gitconfig_path = dotfile_path('.gitconfig')


def run(store):
    gitconfig.run(store)
