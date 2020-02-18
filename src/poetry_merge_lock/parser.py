"""Line-based parser for files with merge conflicts."""
from enum import Enum
from typing import Iterator, Optional, Sequence, Tuple


class Token(Enum):
    """Token for parsing files with merge conflicts."""

    CONFLICT_START = "<<<<<<< "
    CONFLICT_SEPARATOR = "=======\n"
    CONFLICT_END = ">>>>>>> "
    DEFAULT = ""


def tokenize(line: str) -> Token:
    """Return the token for the line."""
    for token in Token:
        if line.startswith(token.value):
            return token

    return Token.DEFAULT  # pragma: no cover


class State(Enum):
    """Parser state for files with merge conflicts."""

    COMMON = 1
    OURS = 2
    THEIRS = 3


class UnexpectedTokenError(ValueError):
    """The parser encountered an unexpected token."""

    def __init__(self, token: Token) -> None:
        """Constructor."""
        super().__init__("unexpected token {}".format(token))


state_transitions = {
    (State.COMMON, Token.CONFLICT_START): State.OURS,
    (State.OURS, Token.CONFLICT_SEPARATOR): State.THEIRS,
    (State.THEIRS, Token.CONFLICT_END): State.COMMON,
}


def parse_line(line: str, state: State) -> Tuple[Token, State]:
    """Parse a single line in a file with merge conflicts.

    Args:
        line: The line to be parsed.
        state: The current parser state.

    Returns:
        A pair, consisting of the token for the line, and the new parser state.

    Raises:
        UnexpectedTokenError: The parser encountered an unexpected token.
    """
    token = tokenize(line)

    for (valid_state, the_token), next_state in state_transitions.items():
        if token is the_token:
            if state is not valid_state:
                raise UnexpectedTokenError(token)
            return token, next_state

    return token, state


def parse_lines(lines: Sequence[str]) -> Iterator[Tuple[Optional[str], Optional[str]]]:
    """Parse a sequence of lines with merge conflicts.

    Args:
        lines: The sequence of lines to be parsed.

    Yields:
        Pairs, where first item in each pair is a line in *our* version, and
        the second, in *their* version. An item is ``None`` if the line does
        not occur in that version.

    Raises:
        ValueError: A conflict marker was not terminated.
    """
    state = State.COMMON

    for line in lines:
        token, state = parse_line(line, state)

        if token is not Token.DEFAULT:
            continue

        if state is State.OURS:
            yield line, None
        elif state is State.THEIRS:
            yield None, line
        else:
            yield line, line

    if state is not State.COMMON:
        raise ValueError("unterminated conflict marker")


def parse(lines: Sequence[str]) -> Tuple[Sequence[str], Sequence[str]]:
    """Parse a sequence of lines with merge conflicts.

    Args:
        lines: The sequence of lines to be parsed.

    Returns:
        A pair of sequences of lines. The first sequence corresponds to *our*
        version, and the second, to *their* version.
    """
    result = parse_lines(lines)
    ours, theirs = zip(*result)
    return (
        [line for line in ours if line is not None],
        [line for line in theirs if line is not None],
    )
