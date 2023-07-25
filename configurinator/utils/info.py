import functools
import itertools
import re

from utils.env import run


@functools.total_ordering
class Version:
    def __init__(self, *version: tuple[int], delimiter: str = '.'):
        self.version = version
        self.delimiter = delimiter

    def init_str(self, version: str):
        self.version = tuple([int(i) for i in version.split(self.delimiter)])
        return self

    def __repr__(self):
        return f"Version(*{self.version}, delimiter='{self.delimiter}')"

    def __str__(self):
        return self.delimiter.join([str(i) for i in self.version])

    def __eq__(self, other):
        if not other:
            return False

        for i, j in itertools.zip_longest(self.version, other.version, fillvalue=0):
            if i != j:
                return False
        return True

    def __lt__(self, other):
        if not other:
            return False

        for i, j in itertools.zip_longest(self.version, other.version, fillvalue=0):
            if i < j:
                return True
            # if the most significant version number that is not equal visited so far is greater then we are sure the version is not less
            if i > j:
                return False
        return False

    # other ordering operations are generated using functools.total_ordering


def get_version(command: str, arguments: list[str] = ['--version']) -> Version:
    output = run(command, *arguments)
    match = re.search(r'(?:\d+(\D))+\d+', output)
    version = Version(delimiter=match.group(1)).init_str(match.group(0))
    print(f'Found {command} version {version}')
    return version
