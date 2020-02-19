"""Merge tool for Poetry lock files at the TOML level."""
import itertools
from typing import Any, Dict, List

import tomlkit
from tomlkit.api import _TOMLDocument, Key, Table


class MergeConflictError(ValueError):
    """An item in the TOML document cannot be merged."""

    def __init__(self, keys: List[Key], ours: Any, theirs: Any) -> None:
        """Constructor."""
        message = "Merge conflict at {}, merging {!r} and {!r}".format(
            ".".join(str(key) for key in keys), ours, theirs
        )
        super().__init__(message)


def merge_locked_packages(value: List[Table], other: List[Table]) -> List[Table]:
    """Merge two TOML arrays containing locked packages.

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
    """Merge two TOML tables containing package files.

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


def merge(value: _TOMLDocument, other: _TOMLDocument) -> _TOMLDocument:
    """Merge two versions of lock data.

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
