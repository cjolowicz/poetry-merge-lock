"""Parser tests."""
import pytest

from poetry_merge_lock import parser


def test_tokenize_empty_string() -> None:
    """The empty string produces a default token."""
    assert parser.Token.DEFAULT == parser.tokenize("")


def test_tokenize_conflict_start() -> None:
    """The start marker of a merge conflict produces the corresponding token."""
    line = "<<<<<<< HEAD\n"
    assert parser.Token.CONFLICT_START == parser.tokenize(line)


def test_parse_expected_token() -> None:
    """The separator of a merge conflict switches to THEIRS state."""
    line = "=======\n"
    assert (parser.Token.CONFLICT_SEPARATOR, parser.State.THEIRS) == parser.parse_line(
        line, parser.State.OURS
    )


def test_parse_unexpected_token() -> None:
    """The separator of a merge conflict cannot occur in COMMON state."""
    line = "=======\n"
    with pytest.raises(parser.UnexpectedTokenError):
        parser.parse_line(line, parser.State.COMMON)


def test_parse_conflict() -> None:
    """A merge conflict produces a version for each side."""
    text = """\
<<<<<<< HEAD
content-hash = "5ef979fbca4b14a24b7f3e1f3f8831dc942a007d3872af8cc8fbf0dd9c4dc40b"
=======
content-hash = "44b4f46d0544df5414531b73cb9220196b616acd60143d76877c7d959e649c45"
>>>>>>> Add foobar 1.0.0
"""

    lines = text.splitlines(keepends=True)
    ours, theirs = parser.parse(lines)

    assert ours == [lines[1]]
    assert theirs == [lines[3]]


def test_unterminated_conflict_marker() -> None:
    """Unterminated conflict markers result in an exception."""
    lines = ["""<<<<<<< HEAD\n"""]
    with pytest.raises(ValueError):
        parser.parse(lines)
