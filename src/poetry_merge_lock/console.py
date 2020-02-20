"""Command-line interface."""
import click
from poetry.factory import Factory
from poetry.utils._compat import Path

from . import __version__
from .core import merge_lock


@click.command()
@click.option(
    "--print-content-hash",
    is_flag=True,
    help="Print the content hash (`metadata.content-hash`)",
)
@click.version_option(version=__version__)
def main(print_content_hash: bool) -> None:
    """Merge the lock file of a Poetry project.

    This is a tool for resolving merge conflicts in the lock file of
    Poetry, a packaging and dependency manager for Python. If the merge
    conflicts cannot be resolved by this tool, you can use the
    --print-content-hash option to compute the content hash for the
    metadata.content-hash entry, and resolve the conflicts manually.
    \f

    Args:
        print_content_hash: Print the content hash.
    """
    poetry = Factory().create_poetry(Path.cwd())

    if print_content_hash:
        click.echo(poetry.locker._content_hash)
    else:
        merge_lock(poetry)
