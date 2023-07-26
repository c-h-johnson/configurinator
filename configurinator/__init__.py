from configurinator import packages
from configurinator.utils.env import is_exe, is_root


def _user() -> None:
    if not packages.package_manager.root:
        packages.run()

    if is_exe('alacritty'):
        from config import alacritty
        alacritty.run()
    if is_exe('bash'):
        from config import bash
        bash.run()
    if is_exe('firefox'):
        from config import firefox
        firefox.run()
    if is_exe('git'):
        from config import git
        git.run()
    if is_exe('hx') or is_exe('helix'):
        from config import helix
        helix.run()
    if is_exe('mako'):
        from config import mako
        mako.run()
    if is_exe('nvim'):
        from config import neovim
        neovim.run()
    if is_exe('pylsp'):
        from config import ruff
        ruff.run()
    if is_exe('python') or is_exe('python3'):
        from config import python
        python.run()
    if is_exe('sway'):
        from config import sway
        sway.run()


def _root() -> None:
    if packages.package_manager.root:
        packages.install()

    if is_exe('makepkg'):
        from config import makepkg
        makepkg.run()
    if is_exe('pacman'):
        from config import pacman
        pacman.run()
    if is_exe('systemctl'):
        from config import systemd
        systemd.run()


def main():
    if is_root():
        _root()
    else:
        _user()
