from configurinator.config.sway import main_config
from configurinator.utils.env import dotfile_path

root = dotfile_path('.config/sway')


def run():
    main_config.run()
