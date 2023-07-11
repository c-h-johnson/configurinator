from utils.env import is_exe, is_root

if not is_root():
    raise RuntimeError('Need to run as root')

import packages
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
