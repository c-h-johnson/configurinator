from configurinator.packages.definitions import Package, PackageChoice, PackageList

browser_web = PackageChoice(
    Package('firefox'),
    Package('chromium'),
)

all_packages = [
    browser_web,
    Package('libnotify', why='`notify-send` command to send notifications'),
]


def add(base: PackageList, desktop: bool = False):
    """Add desktop applications.

    Can only be ran from `./desktops.py`
    if ran at module level there is no knowledge of if a desktop enviroment is installed.
    """
    if not desktop:
        return

    for i in all_packages:
        base.add(i)
