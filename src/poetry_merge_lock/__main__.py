"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Poetry Merge Lock."""


if __name__ == "__main__":
    main(prog_name="poetry-merge-lock")  # pragma: no cover
