from abc import ABC, abstractmethod
from collections import namedtuple

from configurinator.packages.package_managers import PACKAGE_MANAGER
from configurinator.persist.store import PersistStore
from configurinator.utils.ui import select, yesno

"""
packages: list[str]
response: Optional[bool]
"""
ProposalResponse = namedtuple('ProposalResponse', ['packages', 'response'], defaults=[None])


class PackageEntry(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _installed(self) -> bool:
        pass

    @property
    def installed(self) -> bool:
        return self._installed()

    @abstractmethod
    def propose(self, store: PersistStore, previous_response: bool | None = None) -> ProposalResponse:
        """Ask the user to select packages."""


class PackageList(PackageEntry):
    def __init__(self, *packages: list[PackageEntry]):
        super().__init__()

        self.packages = packages

    def __str__(self) -> str:
        return ','.join(str(i) for i in self.packages)

    def add(self, *packages: list[PackageEntry]):
        self.packages += packages

    def _installed(self) -> bool:
        return all(i.installed for i in self.packages)

    def propose(self, store: PersistStore, previous_response: bool | None = None) -> ProposalResponse:
        packages_to_install = []
        for i in self.packages:
            result = i.propose(store, previous_response)
            packages_to_install += result.packages
            previous_response = result.response
        return ProposalResponse(packages_to_install)


class Package(PackageEntry):
    def __init__(self, name, why: str | None = None, **kwargs):
        """If in doubt `name` should be the name of the binary available `**kwargs` correspond to the `name`s defined in `./package_managers.py`."""
        super().__init__()

        self.name = kwargs.get(PACKAGE_MANAGER.name, name) if PACKAGE_MANAGER else None
        self.why = why

        self.depends = PackageList()

    def __str__(self) -> str:
        return self.name

    def depend(self, *args):
        self.depends.add(*args)
        return self

    def _installed(self) -> bool:
        return PACKAGE_MANAGER.is_installed(self.name)

    def propose(self, store: PersistStore, previous_response: bool | None = None) -> ProposalResponse:
        install = False
        propose_depends = False
        if not self.name:
            # ignore this package and its depends
            pass
        elif self.installed:
            propose_depends = True
        elif previous_response is not None:
            install = previous_response
        else:
            prompt = f'Install {self.name}?'
            if self.why:
                prompt += f' ({self.why})'
            install, all_selected = store.use(f'packages.package.{self.name}', lambda: yesno(prompt))
            if all_selected:
                # if in a `PackageList` every subsequent package will also be installed without user interaction
                previous_response = install

        packages_to_install = [self.name] if install else []
        if install or propose_depends:
            packages_to_install += self.depends.propose(store).packages

        return ProposalResponse(packages_to_install, previous_response)


class PackageChoice(PackageList):
    """A mutually exclusive package selection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _installed(self) -> bool:
        return any(i.installed for i in self.packages)

    def propose(self, store: PersistStore, previous_response: bool | None = None) -> ProposalResponse:
        choice = None
        if not self.installed:
            options = [i.name for i in self.packages if i.name]
            choice = store.use(f'packages.choice.{self}', lambda: select(*options, none=True, default=options[0]))

        packages_to_install = []
        for i in self.packages:
            if i.name == choice or i.installed:
                # set `previous_response` to True as this package has just been chosen ergo no need for a second prompt
                packages_to_install += i.propose(store, previous_response=True).packages

        return ProposalResponse(packages_to_install, previous_response)
