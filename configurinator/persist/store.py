import json
import os
from collections.abc import Callable
from typing import TypeAlias, TypeVar

from configurinator.common import File
from configurinator.utils.env import dotfile_path, is_root
from configurinator.utils.ui import YesNoResult

T = TypeVar('T')

Primative: TypeAlias = bool | int | float | str
Custom: TypeAlias = File | YesNoResult
CustomSerialized: TypeAlias = dict[str, Primative]

if is_root():
    ORIGINAL_USER = os.environ.get('SUDO_USER')
    ORIGINAL_UID = int(os.environ.get('SUDO_UID'))
    ORIGINAL_GID = int(os.environ.get('SUDO_GID'))

REL_CONFIG_DIR = '.config/configurinator'
CONFIG_DIR = f'/home/{ORIGINAL_USER}/{REL_CONFIG_DIR}' if is_root() else dotfile_path(REL_CONFIG_DIR)
PERSIST_PATH = os.path.join(CONFIG_DIR, 'persist.json')


def serialize(obj: Primative | Custom) -> Primative | CustomSerialized:
    if isinstance(obj, Primative):
        return obj
    if isinstance(obj, File):
        return {'type': 'File', 'path': obj.path}
    if isinstance(obj, YesNoResult):
        return {'type': 'YesNoResponse', 'result': obj.result, 'all': obj.all}

    msg = f'cannot serialize object of type {type(obj)}'
    raise TypeError(msg)


def deserialize(obj: Primative | CustomSerialized) -> Primative | Custom:
    if isinstance(obj, Primative):
        return obj

    if not isinstance(obj, dict):
        msg = f'cannot deserialize object of type {type(obj)}'
        raise TypeError(msg)

    match obj['type']:
        case 'File':
            return File(obj['path'])
        case 'YesNoResponse':
            return YesNoResult(obj['result'], obj['all'])
        case unknown:
            msg = f'cannot deserialize object of type {unknown}'
            raise TypeError(msg)


class PersistStore:
    def __init__(self):
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        self.file = None
        self.data = None
        self.module = None

    def __enter__(self):
        if not os.path.isfile(PERSIST_PATH):
            with open(PERSIST_PATH, 'w') as f:
                f.write('{}')
        with open(PERSIST_PATH) as f:
            self.data = json.load(f)

        self.file = open(PERSIST_PATH, 'w')

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.truncate()
        json.dump(self.data, self.file)
        self.file.close()

        # if the script was ran as root, we must reset the permissions of the files in the user dir
        if is_root():
            for path in [CONFIG_DIR, PERSIST_PATH]:
                os.chown(path, ORIGINAL_UID, ORIGINAL_GID)

    def use(self, name: str, function: Callable[[], T]) -> T:
        if name in self.data:
            return deserialize(self.data[name])

        result = function()
        self.data[name] = serialize(result)
        return result
