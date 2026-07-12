"""Generic operations derived from a token stream.

These work on any ``List[Token]`` regardless of which engine produced it, so the
regex and pygments backends share one implementation of remove/extract/count,
normalization and metrics.
"""
import math
from collections import Counter
from typing import List, Set

from .metrics import CodeStats, Halstead
from .tokens import Token, TokenType

# Language-agnostic decision points used for the approximate cyclomatic complexity.
DECISION_KEYWORDS = frozenset({
    'if', 'elif', 'elseif', 'for', 'foreach', 'while', 'case', 'when', 'catch',
    'except', 'and', 'or', 'unless',
})
# Substrings within operator tokens that add a decision (&&, ||, ternary ?).
DECISION_OPERATORS = ('&&', '||', '?')

_OPERAND_TYPES = (TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING)
_OPEN_BRACKETS, _CLOSE_BRACKETS = set('([{'), set(')]}')


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


def halstead(tokens: List[Token]) -> Halstead:
    """Compute :class:`~PyReprism.metrics.Halstead` measures from ``tokens``."""
    operators: Counter = Counter()
    operands: Counter = Counter()
    for tok in tokens:
        if tok.type in (TokenType.OPERATOR, TokenType.KEYWORD):
            operators[tok.value] += 1
        elif tok.type is TokenType.OTHER and tok.value.strip():
            operators[tok.value] += 1
        elif tok.type in _OPERAND_TYPES:
            operands[tok.value] += 1
    return Halstead(
        distinct_operators=len(operators), distinct_operands=len(operands),
        total_operators=sum(operators.values()), total_operands=sum(operands.values()),
    )


def cyclomatic(tokens: List[Token], decision_keywords: Set[str] = DECISION_KEYWORDS) -> int:
    """Approximate McCabe cyclomatic complexity: ``1 + decision points``.

    Counts branch keywords plus ``&&``/``||``/``?`` operators. This is a
    token-level approximation; an exact value needs a control-flow graph.
    """
    complexity = 1
    for tok in tokens:
        # Branch words are usually KEYWORD, but word-operators (and/or) can land
        # as IDENTIFIER in the generic lexer, so check both.
        if (tok.type in (TokenType.KEYWORD, TokenType.IDENTIFIER)
                and tok.value.lower() in decision_keywords):
            complexity += 1
        elif tok.type is TokenType.OPERATOR:
            for op in DECISION_OPERATORS:
                complexity += tok.value.count(op)
    return complexity


def max_nesting_depth(tokens: List[Token]) -> int:
    """Maximum bracket nesting depth (``()``/``[]``/``{}``), ignoring strings/comments."""
    depth = deepest = 0
    for tok in tokens:
        if tok.type in (TokenType.STRING, TokenType.COMMENT):
            continue
        for ch in tok.value:
            if ch in _OPEN_BRACKETS:
                depth += 1
                deepest = max(deepest, depth)
            elif ch in _CLOSE_BRACKETS:
                depth = max(0, depth - 1)
    return deepest


def maintainability_index(tokens: List[Token], code_lines: int) -> float:
    """SEI-normalized Maintainability Index in ``[0, 100]`` (higher is better)."""
    volume = halstead(tokens).volume
    complexity = cyclomatic(tokens)
    raw = (171
           - 5.2 * math.log(max(volume, 1))
           - 0.23 * complexity
           - 16.2 * math.log(max(code_lines, 1)))
    return round(max(0.0, min(100.0, raw * 100 / 171)), 2)
