"""Test cases for the __main__ module."""
import re

from click.testing import CliRunner
import pytest

from poetry_merge_lock import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_main_prints_content_hash(runner: CliRunner) -> None:
    """It prints the content hash."""
    result = runner.invoke(console.main, ["--print-content-hash"])
    pattern = re.compile("[0-9a-f]{64}\n")
    assert pattern.match(result.output) is not None
