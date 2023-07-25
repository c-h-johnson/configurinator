import abc
import os
import urllib.request

from utils.env import is_exe, run


class ExecutableNotFoundError(OSError):
    pass


class Exe:
    """An executable file accessible on $PATH."""

    def __init__(self, name: str, *args: tuple[str, ...]):
        self.name = name
        self.args = list(args)

    def _can_run(self, func):
        def inner(self_inner, *args, **kwargs):
            if not self_inner.exists:
                raise ExecutableNotFoundError

            return func(self_inner, *args, **kwargs)

        return inner

    @property
    @_can_run
    def command(self) -> str:
        return ' '.join([self.name, *self.args])

    @property
    def exists(self) -> bool:
        return is_exe(self.name)

    @_can_run
    def run(self, *args: tuple[str, ...]) -> str:
        run(self.name, *self.args, *args)


class File:
    """A file that exists on the filesystem."""

    def __init__(self, path: str):
        self._path = path

    @property
    def exists(self) -> bool:
        return os.path.isfile(self._path)

    @property
    def path(self) -> str:
        if not self.exists:
            msg = f'{self._path} does not exist'
            raise FileNotFoundError(msg)

        return self._path

    @property
    def name(self) -> str:
        return os.path.basename(self.path)


class RemoteResource(abc.ABC):
    """A remote resource that can be downloaded and possibly updated."""

    def __init__(self, url: str):
        self._url = url

    @property
    def url(self) -> str:
        return self._url

    @abc.abstractmethod
    def download(self):
        """Download this resource to the specified path. Must be implemented."""

    @abc.abstractmethod
    def update(self):
        """Update the resource at the specified path. Must be implemented if the source supports checking for changes without downloading everything."""


class Re(RemoteResource):
    def __init__(self, url: str, name: str | None = None):
        """Single remote file.

        Args:
        ----
        url: URL of file
        name: override the name of the file from url
        """
        super().__init__(url)

        if not name:
            name = os.path.basename(url)
        self.name = name

    def download(self, path: str) -> File:
        if not os.path.isdir(path):
            os.mkdir(path)

        full_path = os.path.join(path, self.name)
        if os.path.exists(full_path):
            print(f'{full_path} already exists, skipping download')
        else:
            print(f'downloading {self._url} to {full_path}')
            urllib.request.urlretrieve(url=self._url, filename=full_path)

        return File(full_path)


GIT = Exe('git')


class GitResource(RemoteResource):
    """A git repository that can be cloned and pulled."""

    def __init__(self, url: str):
        super().__init__(url)

    def download(self, path: str):
        GIT.run('clone', self._url, path)

    def update(self, path: str):
        GIT.run('-C', path, 'pull')


class RemoteBundle:
    """A superset of `RemoteResource` that includes auxilary information that is required to automatically extract and select the required parts."""

    def __init__(self, name: str, resource: RemoteResource, files: list[str]):
        if not files:
            msg = 'files is empty'
            raise IndexError(msg)

        self._name = name
        self._resource = resource
        self._files = files

    @property
    def name(self) -> str:
        return self._name

    @property
    def resource(self) -> RemoteResource:
        return self._resource

    @property
    def files(self) -> list[str]:
        return self._files.copy()


class RemoteBundleList:
    def __init__(self, *bundles: list[RemoteBundle]):
        self._bundles = {i.name: i for i in bundles}

    @property
    def bundles(self) -> dict[str, RemoteBundle]:
        return self._bundles.copy()

    def get(self, name: str) -> RemoteBundle:
        return self._bundles.get(name)
