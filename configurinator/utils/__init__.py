from collections.abc import Iterator
import importlib
import pkgutil
from types import ModuleType


# this function should stay here unless similar abstractions can be grouped with this in a new file
def iter_submodules(base_path: list[str], base_dir: str) -> Iterator[ModuleType]:
    for submodule in pkgutil.iter_modules(base_path):
        yield importlib.import_module(base_dir + submodule.name)
