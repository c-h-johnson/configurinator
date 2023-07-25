import os
import pathlib
import platform
import shutil
import subprocess


def cpu_name() -> str:
    model_name = None
    with open('/proc/cpuinfo') as f:
        for i in f.readlines():
            if i.startswith('model name'):
                model_name = i
                break

    if model_name is None:
        return ''

    return model_name[model_name.find(':')+2:-1]


def run(*args: tuple[str, ...]) -> str:
    res = subprocess.check_output(args)
    return res.decode('utf-8')


def rm(path: str) -> bool:
    """Remove `path`.

    Args:
    ----
    path: path to remove
    Returns:
        bool: if the path existed
    """
    if (exists := os.path.isfile(path)):
        os.remove(path)
    elif (exists := os.path.isdir(path)):
        shutil.rmtree(path)

    if exists:
        print(f'Removed {path}')

    return exists


def ln(target, link_name):
    """Create a symbolic link `link_name` that points to `target`."""
    if not os.path.islink(link_name):
        rm(link_name)
        os.symlink(target, link_name)
        print(f'created symlink {link_name} -> {target}')


def dotfile_path(fname: str) -> str:
    """Get the full path of a dotfile in the ~/ directory."""
    return str(pathlib.Path(f'~/{fname}').expanduser())


def is_exe(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    detected = shutil.which(name) is not None
    if not detected and platform.system() == 'Darwin':
        try:
            run('open', '-n', '-a', name, '--args', '--version')
            detected = True
        except subprocess.CalledProcessError:
            pass
    if detected:
        print(f'Detected {name}')
    return detected


def is_root() -> bool:
    return os.geteuid() == 0


def select_font(*fonts: list[str], default: str) -> str:
    """Select a font from fonts passed as arguements.

    Select first available font with fallback to `default`.
    """
    available_fonts = run('fc-list')
    for font in fonts:
        if font in available_fonts:
            return font
    return default
