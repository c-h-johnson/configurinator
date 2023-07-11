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
    )
)

programming = PackageList(
    Package('python', apt='python3', brew='').depend(
        Package('python-lsp-server', apt='').depend(
            PackageChoice(
                Package('yapf', apt='yapf3', why='code formatting (preferred over autopep8)'),
                Package('autopep8', apt='python3-autopep8', why='code formatting'),
            ),
            Package('python-mccabe', apt='python3-mccabe', why='linter for complexity checking'),
            Package('python-pycodestyle', apt='python3-pycodestyle', why='linter for style checking'),
            Package('python-pyflakes', apt='python3-pyflakes', why='linter to detect various errors'),
            Package('python-rope', apt='python3-rope', why='Completions and renaming'),
        ),
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
