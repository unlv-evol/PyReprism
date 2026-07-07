"""Generic operations derived from a token stream.

These work on any ``List[Token]`` regardless of which engine produced it, so the
regex and pygments backends share one implementation of remove/extract/count,
normalization and metrics.
"""
from typing import List

from .metrics import CodeStats
from .tokens import Token, TokenType


def remove(tokens: List[Token], ttype: TokenType) -> str:
    return ''.join(t.value for t in tokens if t.type is not ttype)


def extract(tokens: List[Token], ttype: TokenType) -> List[str]:
    return [t.value for t in tokens if t.type is ttype]


def count(tokens: List[Token], ttype: TokenType) -> int:
    return sum(1 for t in tokens if t.type is ttype)


def normalize(tokens: List[Token], *, rename_identifiers: bool = True,
              mask_numbers: bool = True, mask_strings: bool = True,
              drop_comments: bool = True, collapse_whitespace: bool = False,
              identifier_prefix: str = 'VAR', number_placeholder: str = '0',
              string_placeholder: str = '"STR"') -> str:
    mapping = {}
    parts = []
    for tok in tokens:
        t = tok.type
        if t is TokenType.COMMENT:
            if not drop_comments:
                parts.append(tok.value)
        elif t is TokenType.STRING and mask_strings:
            parts.append(string_placeholder)
        elif t is TokenType.NUMBER and mask_numbers:
            parts.append(number_placeholder)
        elif t is TokenType.IDENTIFIER and rename_identifiers:
            name = mapping.get(tok.value)
            if name is None:
                name = f"{identifier_prefix}{len(mapping) + 1}"
                mapping[tok.value] = name
            parts.append(name)
        elif t is TokenType.WHITESPACE and collapse_whitespace:
            parts.append(' ')
        else:
            parts.append(tok.value)
    return ''.join(parts)


def stats(tokens: List[Token], source: str) -> CodeStats:
    counts = {t: 0 for t in TokenType}
    code_lines = set()
    comment_lines = set()
    for tok in tokens:
        counts[tok.type] += 1
        if tok.type is TokenType.WHITESPACE:
            continue
        span = range(tok.line, tok.line + tok.value.count('\n') + 1)
        target = comment_lines if tok.type is TokenType.COMMENT else code_lines
        target.update(span)
    total = len(source.splitlines())
    code = len(code_lines)
    comment = len(comment_lines - code_lines)
    blank = max(total - code - comment, 0)
    return CodeStats(
        lines=total, code_lines=code, comment_lines=comment, blank_lines=blank,
        characters=len(source),
        comment_tokens=counts[TokenType.COMMENT],
        string_tokens=counts[TokenType.STRING],
        number_tokens=counts[TokenType.NUMBER],
        keyword_tokens=counts[TokenType.KEYWORD],
        identifier_tokens=counts[TokenType.IDENTIFIER],
        operator_tokens=counts[TokenType.OPERATOR],
    )
