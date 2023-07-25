from config.bash import (
        alias, alternative, arguments, env, helix, history, neovim, profile, prompt,
        python,
        )
from utils.env import dotfile_path

profile_path = dotfile_path('.bash_profile')
bashrc = dotfile_path('.bashrc')


def run():
    alias.run()
    alternative.run()
    arguments.run()
    env.run()
    helix.run()
    history.run()
    neovim.run()
    profile.run()
    prompt.run()
    python.run()
