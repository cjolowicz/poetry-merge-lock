"""Parser tests."""
import pytest
from poetry_merge_lock import parser


def test_tokenize_empty_string():
    """The empty string produces a default token."""
    assert parser.Token.DEFAULT == parser.tokenize("")


def test_tokenize_conflict_start():
    """The start marker of a merge conflict produces the corresponding token."""
    line = "<<<<<<< HEAD\n"
    assert parser.Token.CONFLICT_START == parser.tokenize(line)


def test_parse_expected_token():
    """The separator of a merge conflict switches to THEIRS state."""
    line = "=======\n"
    assert (parser.Token.CONFLICT_SEPARATOR, parser.State.THEIRS) == parser.parse_line(
        line, parser.State.OURS
    )


def test_parse_unexpected_token():
    """The separator of a merge conflict cannot occur in COMMON state."""
    line = "=======\n"
    with pytest.raises(parser.UnexpectedTokenError):
        parser.parse_line(line, parser.State.COMMON)
