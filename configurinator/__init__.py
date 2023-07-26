from configurinator import packages
from configurinator.utils.env import is_exe, is_root


def _user() -> None:
    if not packages.package_manager.root:
        packages.run()

    if is_exe('alacritty'):
        from configurinator.config import alacritty
        alacritty.run()
    if is_exe('bash'):
        from configurinator.config import bash
        bash.run()
    if is_exe('firefox'):
        from configurinator.config import firefox
        firefox.run()
    if is_exe('git'):
        from configurinator.config import git
        git.run()
    if is_exe('hx') or is_exe('helix'):
        from configurinator.config import helix
        helix.run()
    if is_exe('mako'):
        from configurinator.config import mako
        mako.run()
    if is_exe('nvim'):
        from configurinator.config import neovim
        neovim.run()
    if is_exe('pylsp'):
        from configurinator.config import ruff
        ruff.run()
    if is_exe('python') or is_exe('python3'):
        from configurinator.config import python
        python.run()
    if is_exe('sway'):
        from configurinator.config import sway
        sway.run()


def _root() -> None:
    if packages.package_manager.root:
        packages.install()

    if is_exe('makepkg'):
        from configurinator.config import makepkg
        makepkg.run()
    if is_exe('pacman'):
        from configurinator.config import pacman
        pacman.run()
    if is_exe('systemctl'):
        from configurinator.config import systemd
        systemd.run()


def main():
    if is_root():
        _root()
    else:
        _user()
