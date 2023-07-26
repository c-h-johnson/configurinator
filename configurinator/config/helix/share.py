import platform

from configurinator.utils.env import dotfile_path, is_exe
from configurinator.utils.info import Version, get_version

supported = True
if platform.system() in ['Linux', 'Darwin']:
    root = dotfile_path('.config/helix')
    cache_dir = dotfile_path('.cache/helix')
elif platform.system() == 'Windows':
    root = dotfile_path('AppData/Roaming/helix')
    cache_dir = dotfile_path('AppData/Local/helix')
else:
    supported = False

EXE_NAME = None
# some distrobutions such as arch linux rename hx to helix
for i in ['hx', 'helix']:
    if is_exe(i):
        EXE_NAME = i
        break

VERSION = get_version(EXE_NAME) if EXE_NAME else None

CMD_ARGS = []
if VERSION >= Version(22, 12) and platform.system() in ['Linux', 'Darwin']:
    CMD_ARGS += ['--log', '/dev/null']
