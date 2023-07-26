from configurinator.packages.definitions import PackageList
from configurinator.utils import iter_submodules


def add_all(base: PackageList):
    for group in iter_submodules(__path__, 'packages.groups.'):
        group.add(base)
