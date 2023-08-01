import os
import shutil

from configurinator.common import group_exe
from configurinator.config import sway
from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import is_exe
from configurinator.utils.ui import get_bg, select, select_exe, yesno

CMD_LOCK = 'swaylock -f -c 000000'
CMD_IDLE = 'swayidle'

DEFAULT_WALLPAPERS = [
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_768x1024.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_768x1024_Portrait.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_1136x640.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_1136x640_Portrait.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_1366x768.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_1920x1080.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_2048x1536.png',
    '/usr/share/backgrounds/sway/Sway_Wallpaper_Blue_2048x1536_Portrait.png',
]


def exec_cmd(bind, cmd):
    return f'bindsym {bind} exec {cmd}'


def run(store):
    config_path = os.path.join(sway.root, 'config')
    if not os.path.isfile(config_path):
        shutil.copy('/etc/sway/config', config_path)

    with ConfigEditor(config_path, '#') as cfg_edit:
        under = '# Your preferred terminal emulator'
        var = '$term'
        terminal = store.use('sway.terminal', lambda: select_exe(group_exe.TERMINAL.values()))
        cfg_edit.add(f'set {var} {terminal}', under=under, start=True)
        cfg_edit.add(exec_cmd('$mod+Return', var), under='# Start a terminal')

        under = ('# Your preferred application launcher\n'
                 '# Note: pass the final command to swaymsg so that the result'
                 'ing window can be opened\n'
                 '# on the original workspace that the command was run on.')
        var = '$menu'
        if is_exe('wofi'):
            cfg_edit.add(f'set {var} wofi --show run', under=under, start=True)
        cfg_edit.add(exec_cmd('$mod+d', var), under='# Start your launcher')

        # all other usages of l are in the window movements
        cfg_edit.add(exec_cmd('$mod+Ctrl+l', CMD_LOCK), under='# lock')

        cfg_edit.add(
            exec_cmd('$mod+Shift+e', "swaynag -t warning -m 'You pressed the exit shortcut. Do you really want to shutdown?.' -B 'Yes, shutdown' 'poweroff'"),
            under='# Exit sway (logs you out of your Wayland session)',
            replace_matching='exec',
        )

        if store.use('sway.change_bg', lambda: yesno('change the background?').result):
            new_bg = store.use('sway.bg', lambda: get_bg(DEFAULT_WALLPAPERS))
            mode = store.use('sway.bg_mode', lambda: select(
                'stretch',
                'fill',
                'fit',
                'center',
                'tile',
                default='fill',
            ))
            cfg_edit.add(
                f'output * bg {new_bg.path} {mode}',
                under='# Default wallpaper (more resolutions are available in /usr/share/backgrounds/sway/)',
                replace_matching='bg',
            )

        # enable swayidle
        if store.use('sway.swayidle', lambda: yesno('Enable swayidle (lock and screen timeout)?').result):
            cfg_edit.add_lines(
                f'exec {CMD_IDLE} -w \\',
                # lock after 5 minutes
                f"         timeout 300 '{CMD_LOCK}' \\",
                # turn off screen after 10 minutes
                "         timeout 600 'swaymsg \"output * power off\"' resume 'swaymsg \"output * power on\"' \\",
                # lock on sleep
                f"         before-sleep '{CMD_LOCK}'",
                under='### Idle configuration',
            )

        # keyboard layout must be defined in this file else non us+qwerty layouts will not work properly
        layout = store.use('sway.keyboard', lambda: input('enter valid code for keyboard layout (e.g. us, gb, etc.): '))
        under = 'input * {'
        cfg_edit.add(f'    xkb_layout "{layout}"', under=under, enclose='}')

        under = 'bar {'
        cfg_edit.remove('    position top')
        cfg_edit.add('    position bottom', under=under)

        if is_exe('grim') and is_exe('slurp') and is_exe('wl-copy'):
            cfg_edit.add(
                exec_cmd('$mod+Shift+s', 'grim -g "$(slurp)" - | wl-copy'),
                under='# take a screenshot and copy to clipboard',
            )

        cfg_edit.add('default_border none')
        cfg_edit.add('include /etc/sway/config.d/*')
