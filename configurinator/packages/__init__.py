from configurinator.packages import groups
from configurinator.packages.definitions import Package, PackageChoice, PackageList
from configurinator.packages.package_managers import PACKAGE_MANAGER
from configurinator.utils.ui import yesno

base = PackageList(
    Package('bottom', apt=''),
    Package('exa'),
    Package('fd', apt='fd-find'),
    Package('ripgrep'),
    Package('starship', apt=''),
    Package('noto-fonts-emoji', apt='fonts-noto-color-emoji', brew=''),
    PackageChoice(
        Package('helix'),
        Package('neovim'),
        Package('vim'),
        Package('emacs'),
        Package('kakoune'),
    ),
)

programming = PackageList(
    Package('python', apt='python3', brew='').depend(
        Package('python-lsp-server', apt=''),
    ),
    Package('cargo', brew='rust').depend(
        Package('rust-analyzer', apt=''),
    ),
)


def install():
    groups.add_all(base)

    if yesno('are you a programmer?').result:
        base.add(programming)

    install = base.propose().packages

    if install:
        print(f'Installing the following packages: {",".join(install)}')
        PACKAGE_MANAGER.install(install)
        print('Packages installed successfully')
