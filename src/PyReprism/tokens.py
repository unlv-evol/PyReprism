"""Token model shared by the tokenizer and the match/extract APIs."""
from enum import Enum
from typing import NamedTuple


class TokenType(str, Enum):
    """The kind of source-code construct a :class:`Token` represents."""

    COMMENT = "comment"
    STRING = "string"
    NUMBER = "number"
    KEYWORD = "keyword"
    OPERATOR = "operator"
    IDENTIFIER = "identifier"
    WHITESPACE = "whitespace"
    OTHER = "other"

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return self.value


class Token(NamedTuple):
    """A single lexical token located within a source string.

    Tokens are immutable. A named tuple rather than a dataclass keeps their
    construction cheap, since a file yields one token per word, operator, or
    run of whitespace.

    :param type: the :class:`TokenType` of the token.
    :param value: the exact substring the token spans.
    :param start: 0-based start offset in the source.
    :param end: 0-based end offset (exclusive) in the source.
    :param line: 1-based line number of ``start``.
    """

    type: TokenType
    value: str
    start: int
    end: int
    line: int
