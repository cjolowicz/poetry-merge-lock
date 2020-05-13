"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from poetry_merge_lock import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_main_succeeds_with_print_content_hash(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, ["--print-content-hash"])
    assert result.exit_code == 0
