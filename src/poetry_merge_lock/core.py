from enum import Enum
import itertools
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from poetry.poetry import Poetry
from poetry.packages import Package
from poetry.packages.locker import Locker
from poetry.utils._compat import Path
import tomlkit
from tomlkit.api import _TOMLDocument, Key, Table

from .parser import parse_lines


def load_toml_versions(toml_file: Path) -> Tuple[_TOMLDocument, _TOMLDocument]:
    """
    Load a pair of TOML documents from a TOML file with merge conflicts.

    Args:
        toml_file: Path to the lock file.

    Returns:
        A pair of TOML documents, corresponding to *our* version and *their*
        version.
    """

    def load(lines: Sequence[Optional[str]]) -> _TOMLDocument:
        data = "".join(line for line in lines if line is not None)
        return tomlkit.loads(data)

    with toml_file.open() as fp:
        parse_result = parse_lines(fp)
        ours, theirs = zip(*parse_result)
        return load(ours), load(theirs)


class MergeConflictError(ValueError):
    """
    An item in the TOML document cannot be merged.
    """

    def __init__(self, keys: List[Key], ours: Any, theirs: Any):
        message = "Merge conflict at {}, merging {!r} and {!r}".format(
            ".".join(str(key) for key in keys), ours, theirs
        )
        super().__init__(message)


def merge_locked_packages(value: List[Table], other: List[Table]) -> List[Table]:
    """
    Merge two TOML arrays containing locked packages.

    Args:
        value: The packages in *our* version of the lock file.
        other: The packages in *their* version of the lock file.

    Returns:
        The packages obtained from merging both versions.

    Raises:
        MergeConflictError: The lists contain different values for the same package.
    """
    packages: Dict[str, Table] = {}

    for package in itertools.chain(value, other):
        current = packages.setdefault(package["name"], package)
        if package.value != current.value:
            raise MergeConflictError(["package"], current, package)

    return list(packages.values())


def merge_locked_package_files(value: Table, other: Table) -> Table:
    """
    Merge two TOML tables containing package files.

    Args:
        value: The package files in *our* version of the lock file.
        other: The package files in *their* version of the lock file.

    Returns:
        The package files obtained from merging both versions.

    Raises:
        MergeConflictError: The tables contain different files for the same package.
    """
    files = tomlkit.table()

    for key in set(itertools.chain(value, other)):
        a = value.get(key)
        b = other.get(key)
        if None not in (a, b) and a != b:
            raise MergeConflictError(["metadata", "files", key], a, b)
        files[key] = a if a is not None else b

    return files


def merge_lock_data(value: _TOMLDocument, other: _TOMLDocument) -> _TOMLDocument:
    """
    Merge two versions of lock data.

    This function returns a TOML document with the following merged entries:

    * ``package``
    * ``metadata.files``

    Any other entries, e.g. ``metadata.content-hash``, are omitted. They are
    generated from pyproject.toml when the lock data is written to disk.

    Args:
        value: Our version of the lock data.
        other: Their version of the lock data.

    Returns:
        The merged lock data.
    """
    document = tomlkit.document()
    document["package"] = merge_locked_packages(value["package"], other["package"])
    document["metadata"] = {
        "files": merge_locked_package_files(
            value["metadata"]["files"], other["metadata"]["files"]
        ),
    }

    return document


def load_lock_data(locker: Locker) -> _TOMLDocument:
    """
    Load a lock file with merge conflicts.

    Args:
        locker: The locker object.

    Returns:
        The merged TOML document.
    """
    lock_file = Path(locker.lock._path)
    ours, theirs = load_toml_versions(lock_file)
    return merge_lock_data(ours, theirs)


def activate_dependencies(packages: List[Package]) -> None:
    """
    Activate the optional dependencies of every package.

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
    """
    Load the packages from a TOML document with lock data.

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


def save_lock_data(locker: Locker, lock_data: _TOMLDocument, root: Package) -> None:
    """
    Validate the lock data and write it to disk.

    Args:
        locker: The locker object.
        lock_data: The lock data.
        root: The root package of the Poetry project.
    """
    packages = load_packages(locker, lock_data)
    locker.set_lock_data(root, packages)


def merge_lock_file(poetry: Poetry) -> None:
    """
    Resolve merge conflicts in Poetry's lock file.
    """
    lock_data = load_lock_data(poetry.locker)
    save_lock_data(poetry.locker, lock_data, poetry.package)
