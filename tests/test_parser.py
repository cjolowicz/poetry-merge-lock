from poetry_merge_lock import parser

import pytest


def test_tokenize_empty_string():
    assert parser.Token.DEFAULT == parser.tokenize("")


def test_tokenize_conflict_start():
    line = "<<<<<<< HEAD\n"
    assert parser.Token.CONFLICT_START == parser.tokenize(line)


def test_parse_expected_token():
    line = "=======\n"
    assert (parser.Token.CONFLICT_SEPARATOR, parser.State.THEIRS) == parser.parse_line(
        line, parser.State.OURS
    )


def test_parse_unexpected_token():
    line = "=======\n"
    with pytest.raises(parser.UnexpectedTokenError):
        parser.parse_line(line, parser.State.COMMON)
