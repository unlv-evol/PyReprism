"""Span-driven language base for comment syntaxes a regex cannot express.

Most languages declare a ``comment_regex`` and inherit the whole API from
:class:`~PyReprism.languages.base.BaseLanguage`. A few do not fit a regular
expression:

* **Nested block comments** (Odin, V, Jai): ``/* /* */ */`` requires counting
  nesting depth, which a regex cannot do.
* **Column-sensitive comments** (COBOL): a ``*`` in the indicator column marks the
  whole line as a comment.

:class:`ScannedLanguage` handles these by delegating to a single classmethod,
:meth:`ScannedLanguage._comment_spans`, that returns the ``(start, end)`` offsets
of every comment. All comment operations---``match``/``extract``/``count``/%
``remove``---and a consistent :meth:`tokenize` are derived from those spans, so a
scanned language behaves exactly like a regex one (losslessly) without a
``comment_regex``. Code between comments is sub-classified by the inherited
:meth:`~PyReprism.languages.base.BaseLanguage._tokenize_code`.

The module name is underscore-prefixed so it is *not* auto-imported as a language
by ``_load_all_languages``; concrete languages import it explicitly.
"""
from typing import List, Tuple

from ..tokens import Token, TokenType
from .base import BaseLanguage, _line_at, _newline_offsets


class ScannedLanguage(BaseLanguage):
    """A language whose comments are found by a scanner, not a regex."""

    @classmethod
    def _comment_spans(cls, source: str) -> List[Tuple[int, int]]:
        """Return sorted, non-overlapping ``(start, end)`` offsets of comments."""
        raise NotImplementedError

    @classmethod
    def comment_regex(cls):
        raise NotImplementedError(
            f"{cls.__name__} is scanned, not regex-based; use the comment methods."
        )

    @classmethod
    def match_comments(cls, source: str) -> List[Token]:
        newlines = _newline_offsets(source)
        return [Token(TokenType.COMMENT, source[s:e], s, e, _line_at(newlines, s))
                for s, e in cls._comment_spans(source) if e > s]

    @classmethod
    def extract_comments(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_comments(source)]

    @classmethod
    def count_comments(cls, source: str) -> int:
        return len(cls.match_comments(source))

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        segments, pos = [], 0
        for start, end in cls._comment_spans(source_code):
            if start > pos:
                segments.append(source_code[pos:start])
            pos = max(pos, end)
        if pos < len(source_code):
            segments.append(source_code[pos:])
        return segments if isList else ''.join(segments)

    @classmethod
    def tokenize(cls, source: str) -> List[Token]:
        newlines = _newline_offsets(source)
        tokens: List[Token] = []
        pos = 0
        for start, end in cls._comment_spans(source):
            if start > pos:
                cls._tokenize_code(source[pos:start], pos, newlines, tokens)
            if end > start:
                tokens.append(Token(TokenType.COMMENT, source[start:end], start, end,
                                    _line_at(newlines, start)))
            pos = max(pos, end)
        if pos < len(source):
            cls._tokenize_code(source[pos:], pos, newlines, tokens)
        return tokens


# --------------------------------------------------------------- nested C-style
def nested_cstyle_spans(source: str) -> List[Tuple[int, int]]:
    """Comment spans for ``//`` line comments and *nested* ``/* */`` blocks,
    skipping string/char/raw-string literals so a delimiter inside a string is not
    mistaken for a comment."""
    spans: List[Tuple[int, int]] = []
    i, n = 0, len(source)
    while i < n:
        c = source[i]
        if c in '"\'`':
            quote = c
            i += 1
            while i < n:
                if source[i] == '\\' and quote != '`':
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == '/' and i + 1 < n and source[i + 1] == '/':
            start = i
            i += 2
            while i < n and source[i] != '\n':
                i += 1
            spans.append((start, i))
            continue
        if c == '/' and i + 1 < n and source[i + 1] == '*':
            start = i
            depth = 1
            i += 2
            while i < n and depth > 0:
                if source[i] == '/' and i + 1 < n and source[i + 1] == '*':
                    depth += 1
                    i += 2
                elif source[i] == '*' and i + 1 < n and source[i + 1] == '/':
                    depth -= 1
                    i += 2
                else:
                    i += 1
            spans.append((start, i))
            continue
        i += 1
    return spans


class NestedCStyleLanguage(ScannedLanguage):
    """C-style ``//`` and *nested* ``/* */`` comments (Odin, V, Jai, ...)."""

    @classmethod
    def _comment_spans(cls, source: str) -> List[Tuple[int, int]]:
        return nested_cstyle_spans(source)
