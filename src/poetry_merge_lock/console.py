"""Command-line interface."""
import click
from poetry.factory import Factory
from poetry.utils._compat import Path

from . import __version__
from .core import merge_lock


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Merge the lock file of a Poetry project."""
    poetry = Factory().create_poetry(Path.cwd())
    merge_lock(poetry)
