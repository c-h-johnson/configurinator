from configurinator.config.alacritty import alacritty_yml
from configurinator.utils.env import dotfile_path

root = dotfile_path('.config/alacritty')


def run(store):
    alacritty_yml.run(store)
