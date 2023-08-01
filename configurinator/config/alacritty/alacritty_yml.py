import os

from configurinator.common import GitResource, RemoteBundle, RemoteBundleList
from configurinator.config import alacritty
from configurinator.utils.config import ConfigEditor
from configurinator.utils.env import select_font
from configurinator.utils.ui import select_remote_file, yesno

THEMES = RemoteBundleList(
    RemoteBundle(
        'catppuccin',
        GitResource('https://github.com/catppuccin/alacritty.git'),
        ['catppuccin-mocha.yml', 'catppuccin-macchiato.yml', 'catppuccin-frappe.yml', 'catppuccin-latte.yml'],
    ),
)


def run(store):
    with ConfigEditor(os.path.join(alacritty.root, 'alacritty.yml'), '# ') as cfg_edit:
        h0 = 'font:'

        cfg_edit.add('  size: 11', under=h0)

        font = store.use('alacritty.font', lambda: select_font(
                'Source Code Pro',
                'DejaVu Sans Mono',
                default='monospace',
                ))

        h1 = '  normal:'
        cfg_edit.add(h1, under=h0)
        prev = '    style: Regular'
        cfg_edit.add(prev, under=h1)
        cfg_edit.add(f'    family: {font}', under=h1, allow_duplicates=True)

        h1 = '  italic:'
        cfg_edit.add(h1, under=prev)
        prev = '    style: Italic'
        cfg_edit.add(prev, under=h1)
        cfg_edit.add(f'    family: {font}', under=h1, allow_duplicates=True)

        h1 = '  bold:'
        cfg_edit.add(h1, under=prev)
        prev = '    style: Bold'
        cfg_edit.add(prev, under=h1)
        cfg_edit.add(f'    family: {font}', under=h1, allow_duplicates=True)

        h1 = '  bold_italic:'
        cfg_edit.add(h1, under=prev)
        cfg_edit.add('    style: Bold Italic', under=h1)
        cfg_edit.add(f'    family: {font}', under=h1, allow_duplicates=True)

        h0 = 'key_bindings:'
        # spawn new instance in same directory
        cfg_edit.add('  - { key: Return,   mods: Control|Shift, action: SpawnNewInstance }', under=h0)

        h0 = 'import:'

        marker = '  # Theme installed by configurinator'
        if store.use('alacritty.use_theme', lambda: yesno('add a theme to alacritty?').result):
            cfg_edit.add(h0)
            cfg_edit.add(marker, under=h0)
            theme_path = store.use('alacritty.theme', lambda: select_remote_file(THEMES, alacritty.root).path)
            cfg_edit.add(f'  - {theme_path}', under=marker)


if __name__ == '__main__':
    run()
