from packages import groups
from packages.definitions import Package, PackageChoice, PackageList
from packages.package_managers import package_manager
from utils.ui import yesno

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
        package_manager.install(install)
        print('Packages installed successfully')
