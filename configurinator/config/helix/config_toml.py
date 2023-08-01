import glob
import os
import platform

from configurinator.config.helix import share
from configurinator.utils.config import ConfigEditor
from configurinator.utils.info import Version
from configurinator.utils.ui import select

THEMES = []
if platform.system() in ['Linux', 'Darwin']:
    theme_files = glob.glob('/var/lib/helix/runtime/themes/*.toml')
    THEMES = [os.path.splitext(os.path.basename(i))[0] for i in theme_files]

# this might change in future versions
THEME_DEFAULT = 'default'


def run(store):
    with ConfigEditor(os.path.join(share.root, 'config.toml')) as cfg_edit:
        if not cfg_edit.exists('theme'):
            print('no theme set')
            print('select a theme for helix')
            if THEMES:
                theme = store.use('helix.theme', lambda: select(*THEMES, default=THEME_DEFAULT))
            else:
                print('could not locate themes')
                theme = store.use('helix.theme', lambda: input('enter helix theme (leave blank to skip): '))

            if theme:
                cfg_edit.add(f'theme = "{theme}"', start=True)

        under = '[editor]'
        cfg_edit.add('idle-timeout = 0', under=under)
        cfg_edit.add('completion-trigger-len = 1', under=under)
        cfg_edit.add('cursorline = true', under=under)

        if share.VERSION >= Version(22, 12):
            cfg_edit.add('bufferline = "multiple"', under=under)
            cfg_edit.add('auto-save = true', under=under)

        under = '[editor.whitespace.render]'
        cfg_edit.add('newline = "none"', under=under)
        cfg_edit.add('space = "none"', under=under)
        cfg_edit.add('tab = "all"', under=under)
        # non-breaking space
        cfg_edit.add('nbsp = "all"', under=under)

        under = '[editor.indent-guides]'
        cfg_edit.add('render = true', under=under)

        if share.VERSION >= Version(23, 3):
            under = '[editor.soft-wrap]'
            cfg_edit.add('enable = true', under=under)

            under = '[editor.lsp]'
            cfg_edit.add('display-messages = true', under=under)
            cfg_edit.add('display-inlay-hints = true', under=under)


if __name__ == '__main__':
    run()
