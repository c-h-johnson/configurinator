from abc import ABC, abstractmethod
from subprocess import CalledProcessError

from configurinator.utils.env import is_exe, run


class PackageManager(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def install(self, packages: list[str]):
        pass

    @abstractmethod
    def is_installed(self, package: str) -> bool:
        pass


class Alpine(PackageManager):
    name = 'apk'
    root = True

    def install(self, packages: list[str]):
        pass

    def is_installed(self, package: str) -> bool:
        pass


class Arch(PackageManager):
    name = 'pacman'
    root = True

    def install(self, packages: list[str]):
        run('sudo', self.name, '-Sy', '--noconfirm', *packages)

    def is_installed(self, package: str) -> bool:
        try:
            run(self.name, '-Q', package)
        except CalledProcessError:
            return False
        return True


class Brew(PackageManager):
    name = 'brew'
    root = False

    def install(self, packages: list[str]):
        for package in packages:
            run(self.name, 'install', package)

    def is_installed(self, package: str) -> bool:
        try:
            return len(run(self.name, 'ls', '--versions', package)) > 0
        except CalledProcessError:
            return False


class Debian(PackageManager):
    name = 'apt'
    root = True

    def install(self, packages: list[str]):
        run('sudo', self.name, 'install', '-y', *packages)

    def is_installed(self, package: str) -> bool:
        try:
            run('dpkg', '-l', package)
        except CalledProcessError:
            return False
        return True


class Gentoo(PackageManager):
    name = 'emerge'
    root = True

    def install(self, packages: list[str]):
        run('sudo', self.name, *packages)


class OpenSUSE(PackageManager):
    name = 'zypper'
    root = True

    def install(self, packages: list[str]):
        pass

    def is_installed(self, package: str) -> bool:
        pass


class Fedora(PackageManager):
    name = 'dnf'
    root = True

    def install(self, packages: list[str]):
        pass

    def is_installed(self, package: str) -> bool:
        pass


AVAILABLE_PACKAGE_MANAGERS = (
    Alpine,
    Arch,
    Brew,
    Debian,
    Gentoo,
    OpenSUSE,
    Fedora,
)

for i in AVAILABLE_PACKAGE_MANAGERS:
    if is_exe(i.name):
        PACKAGE_MANAGER = i()
        break

if not PACKAGE_MANAGER:
    msg = 'could not find a package manager'
    raise RuntimeError(msg)
print(f'found package manager {PACKAGE_MANAGER.name}')
