import os

from common import group_exe
from config import bash, helix
from utils.config import ConfigEditor
from utils.env import rm


def run():
    with ConfigEditor(bash.bashrc) as cfg_edit:
        under = '# reduce disk writes'

        if helix.share.EXE_NAME:
            command = group_exe.editors[helix.share.EXE_NAME].command
            short_alias = f"alias hx='{command}'"
            cfg_edit.add(short_alias, under=under)
            long_alias = f"alias helix='{command}'"
            cfg_edit.add(long_alias, under=short_alias)

            if '--log' in helix.share.CMD_ARGS:
                # only remove helix.log because the cache directory gets created on startup no matter where the log is
                rm(os.path.join(helix.share.cache_dir, 'helix.log'))


if __name__ == '__main__':
    run()
