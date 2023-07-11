from packages.definitions import Package, PackageList
from packages.groups import desktop_applications
from utils.env import is_exe

installed = []

sway = PackageList(
    Package('wofi', why='launcher for wlroots-based wayland compositors'),
    Package('mako', apt='mako-notifier', why='Lightweight notification daemon for Wayland'),
    Package('grim', why='Screenshot utility for Wayland'),
    Package('slurp', why='Required to select region for grim'),
    Package('wl-clipboard', why='Required to save screenshot to clipboard'),
)
if is_exe('sway'):
    print('sway window manager detected')
    installed.append(sway)


def add(base: PackageList):
    for i in installed:
        base.add(i)

    if installed:
        desktop_applications.add(base, True)
