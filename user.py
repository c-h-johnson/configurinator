from utils.env import is_exe, is_root

if is_root():
    msg = 'Do not run as root'
    raise RuntimeError(msg)

import packages

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
