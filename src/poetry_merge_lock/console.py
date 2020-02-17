"""Command-line interface."""
import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Merge the lock file of a Poetry project."""
