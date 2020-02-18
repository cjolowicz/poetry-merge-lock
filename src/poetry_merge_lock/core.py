"""Core module."""
from typing import List, Sequence, Tuple

from poetry.packages import Package
from poetry.packages.locker import Locker
from poetry.poetry import Poetry
from poetry.utils._compat import Path
import tomlkit
from tomlkit.api import _TOMLDocument

from . import mergetool
from . import parser


def load_toml_versions(toml_file: Path) -> Tuple[_TOMLDocument, _TOMLDocument]:
    """Load a pair of TOML documents from a TOML file with merge conflicts.

    Args:
        toml_file: Path to the lock file.

    Returns:
        A pair of TOML documents, corresponding to *our* version and *their*
        version.
    """
    def load(lines: Sequence[str]) -> _TOMLDocument:  # noqa
        return tomlkit.loads("".join(lines))

    with toml_file.open() as fp:
        ours, theirs = parser.parse(fp)
        return load(ours), load(theirs)


def load(locker: Locker) -> _TOMLDocument:
    """Load a lock file with merge conflicts.

    Args:
        locker: The locker object.

    Returns:
        The merged TOML document.
    """
    lock_file = Path(locker.lock._path)
    ours, theirs = load_toml_versions(lock_file)
    return mergetool.merge(ours, theirs)


def activate_dependencies(packages: List[Package]) -> None:
    """Activate the optional dependencies of every package.

    Activating optional dependencies ensures their inclusion when the lock file
    is written.  Normally, optional dependencies are activated by the solver if
    another package depends on them.  But invoking the solver would result in
    regenerating the lock file from scratch, losing the information in the
    original lock file.  So we activate the dependencies manually instead.  We
    know the solver would activate them because they would not be present in the
    lock file otherwise.

    Args:
        packages: The list of packages.
    """
    for package in packages:
        for dependency in package.requires:
            if dependency.is_optional():
                dependency.activate()


def load_packages(locker: Locker, lock_data: _TOMLDocument) -> List[Package]:
    """Load the packages from a TOML document with lock data.

    Args:
        locker: The locker object.
        lock_data: The lock data.

    Returns:
        The list of packages.
    """
    locker._lock_data = lock_data
    repository = locker.locked_repository(with_dev_reqs=True)
    activate_dependencies(repository.packages)
    return repository.packages


def save(locker: Locker, lock_data: _TOMLDocument, root: Package) -> None:
    """Validate the lock data and write it to disk.

    Args:
        locker: The locker object.
        lock_data: The lock data.
        root: The root package of the Poetry project.
    """
    packages = load_packages(locker, lock_data)
    locker.set_lock_data(root, packages)


def merge_lock(poetry: Poetry) -> None:
    """Resolve merge conflicts in Poetry's lock file."""
    lock_data = load(poetry.locker)
    save(poetry.locker, lock_data, poetry.package)
