"""Tests for the merge tool."""
import textwrap

import pytest
import tomlkit
from tomlkit.api import _TOMLDocument

from poetry_merge_lock import mergetool


@pytest.fixture
def lockfile_with_click() -> _TOMLDocument:
    """Lock file with click 7.0."""
    return tomlkit.loads(
        textwrap.dedent(
            """\
            [[package]]
            category = "main"
            description = "Composable command line interface toolkit"
            name = "click"
            optional = false
            python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"
            version = "7.0"

            [metadata]
            content-hash = "{}"
            python-versions = "^3.7"

            [metadata.files]
            click = [
                {{file = "Click-7.0-py2.py3-none-any.whl", hash = "sha256:{}"}},
                {{file = "Click-7.0.tar.gz", hash = "sha256:{}"}},
            ]
            """.format(
                "b8b75d81010ba6daf4b088e7fcb7b8256c7e3fd21675f7e10a94a192895455f8",
                "2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13",
                "5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7",
            )
        )
    )


@pytest.fixture
def lockfile_with_click6() -> _TOMLDocument:
    """Lock file with click 6.0."""
    return tomlkit.loads(
        textwrap.dedent(
            """\
            [[package]]
            category = "main"
            description = "{}"
            name = "click"
            optional = false
            python-versions = "*"
            version = "6.0"

            [metadata]
            content-hash = "{}"
            python-versions = "^3.7"

            [metadata.files]
            click = [
                {{file = "click-6.0-py2.py3-none-any.whl", hash = "sha256:{}"}},
                {{file = "click-6.0.tar.gz", hash = "sha256:{}"}},
            ]
            """.format(
                "A simple wrapper around optparse for powerful command line utilities.",
                "42b8f14bb20d25fc1171c0b8f9704e7261730b608236f217e6d99a0180579be6",
                "561a954a8740f1fc9c101679f43f3b75499192de1c44fbc05a5c27877047a76f",
                "3972ee95a32181e9069040414dd7c77001e9404c3c4d295300cdca06a8db026d",
            )
        )
    )


@pytest.fixture
def lockfile_with_attrs() -> _TOMLDocument:
    """Lock file with attrs 19.3.0."""
    return tomlkit.loads(
        textwrap.dedent(
            """\
            [[package]]
            category = "main"
            description = "Classes Without Boilerplate"
            name = "attrs"
            optional = false
            python-versions = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*"
            version = "19.3.0"

            [package.extras]
            azure-pipelines = [
                "coverage",
                "hypothesis",
                "pympler",
                "pytest (>=4.3.0)",
                "six",
                "zope.interface",
                "pytest-azurepipelines",
            ]
            dev = [
                "coverage",
                "hypothesis",
                "pympler",
                "pytest (>=4.3.0)",
                "six",
                "zope.interface",
                "sphinx",
                "pre-commit",
            ]
            docs = ["sphinx", "zope.interface"]
            tests = [
                "coverage",
                "hypothesis",
                "pympler",
                "pytest (>=4.3.0)",
                "six",
                "zope.interface",
            ]

            [metadata]
            content-hash = "{}"
            python-versions = "^3.7"

            [metadata.files]
            attrs = [
                {{file = "attrs-19.3.0-py2.py3-none-any.whl", hash = "sha256:{}"}},
                {{file = "attrs-19.3.0.tar.gz", hash = "sha256:{}"}},
            ]
            """.format(
                "ad33bb646f374df7b191737ffe67fdbb18c2e4f24528143c37caafe086c0b6d5",
                "08a96c641c3a74e44eb59afb61a24f2cb9f4d7188748e76ba4bb5edfa3cb7d1c",
                "f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72",
            )
        )
    )


def test_merge_includes_all_packages(
    lockfile_with_attrs: _TOMLDocument, lockfile_with_click: _TOMLDocument
) -> None:
    """All packages are included in the merged document."""
    lockfile = mergetool.merge(lockfile_with_attrs, lockfile_with_click)
    packages = [package["name"] for package in lockfile["package"]]
    assert "attrs" in packages
    assert "click" in packages


def test_merge_fails_on_inconsistent_attributes(
    lockfile_with_click: _TOMLDocument, lockfile_with_click6: _TOMLDocument
) -> None:
    """Packages are not merged if their version differs (or any other attribute)."""
    with pytest.raises(
        mergetool.MergeConflictError, match=r"Merge conflict at package, .*"
    ):
        mergetool.merge(lockfile_with_click, lockfile_with_click6)


def test_merge_fails_on_inconsistent_files(
    lockfile_with_click: _TOMLDocument, lockfile_with_click6: _TOMLDocument
) -> None:
    """Packages are not merged if their associated files differ."""
    files = lockfile_with_click6["metadata"]["files"]["click"]
    value = lockfile_with_click
    # Create a deep copy of `metadata.files` by repeated shallow copying.
    # Unfortunately, copy.deepcopy does not work because tomlkit.items.Bool,
    # used for the `optional` attribute of packages, is compared by id.
    other = lockfile_with_click.copy()
    other["metadata"] = value["metadata"].copy()
    other["metadata"]["files"] = value["metadata"]["files"].copy()
    other["metadata"]["files"]["click"] = files
    with pytest.raises(
        mergetool.MergeConflictError,
        match=r"Merge conflict at metadata\.files\.click, .*",
    ):
        mergetool.merge(value, other)
