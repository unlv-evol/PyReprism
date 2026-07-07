"""Token model shared by the tokenizer and the match/extract APIs."""
from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class Token:
    """A single lexical token located within a source string.

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
