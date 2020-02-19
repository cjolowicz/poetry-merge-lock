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
    """Merge the lock file of a Poetry project."""
    poetry = Factory().create_poetry(Path.cwd())

    if print_content_hash:
        click.echo(poetry.locker._content_hash)
    else:
        merge_lock(poetry)
