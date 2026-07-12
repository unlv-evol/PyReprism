import bisect
import re
from functools import lru_cache
from typing import List, Pattern, Union

from ..metrics import CodeStats
from ..tokens import Token, TokenType

# Shared, language-agnostic patterns used by the generic tokenizer.
_WHITESPACE_RE = re.compile(r'\s+')
_OPERATOR_RE = re.compile(r'[-+*/%=<>!&|^~?]+')


def _newline_offsets(source: str) -> List[int]:
    return [i for i, ch in enumerate(source) if ch == '\n']


def _line_at(newlines: List[int], index: int) -> int:
    """Return the 1-based line number of ``index`` given precomputed newline offsets."""
    return bisect.bisect_right(newlines, index) + 1


class BaseLanguage:
    """Base class for language implementations.

    Subclasses must provide :meth:`file_extension` and :meth:`comment_regex`, and
    typically :meth:`keywords`. They may override :meth:`number_regex`,
    :meth:`operator_regex`, :meth:`string_regex`, :meth:`identifier_regex`, and
    :meth:`keywords_regex`.

    This base centralizes the ``remove``/``extract``/``count``/``match`` operations
    for comments, keywords, numbers, operators, strings and identifiers, plus a
    generic :meth:`tokenize`, so every language inherits the full API for free.
    """

    # ------------------------------------------------------------------ regexes
    @classmethod
    def file_extension(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def keywords(cls) -> List[str]:
        return []

    @classmethod
    @lru_cache(maxsize=None)
    def keywords_regex(cls) -> Pattern:
        words = [w for w in (cls.keywords() or []) if w]
        if not words:
            # match nothing
            return re.compile(r"(?!x)x")
        return re.compile(r'\b(' + '|'.join(words) + r')\b', re.IGNORECASE)

    @classmethod
    def comment_regex(cls) -> Pattern:
        """Return a compiled regex with named groups 'comment' and 'noncomment'."""
        raise NotImplementedError()

    @classmethod
    def number_regex(cls) -> Pattern:
        return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> Pattern:
        return re.compile(r'[-+*/%=<>!&|^~?]+')

    @classmethod
    def string_regex(cls) -> Pattern:
        """Default string-literal matcher: single- or double-quoted with escapes."""
        return re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')

    @classmethod
    def identifier_regex(cls) -> Pattern:
        return re.compile(r'[A-Za-z_]\w*')

    # ---------------------------------------------------------------- internals
    @classmethod
    def _match_spans(cls, regex: Pattern, source: str, ttype: TokenType) -> List[Token]:
        """Return non-empty matches of ``regex`` in ``source`` as :class:`Token`s."""
        newlines = _newline_offsets(source)
        tokens = []
        for m in regex.finditer(source):
            if m.end() > m.start():  # skip zero-width matches
                tokens.append(Token(ttype, m.group(), m.start(), m.end(),
                                    _line_at(newlines, m.start())))
        return tokens

    # ----------------------------------------------------------------- comments
    @classmethod
    def match_comments(cls, source: str) -> List[Token]:
        """Return every comment in ``source`` as a :class:`Token` with position info."""
        newlines = _newline_offsets(source)
        tokens = []
        for m in cls.comment_regex().finditer(source):
            # A match is a comment when it did NOT bind the 'noncomment' group.
            if m.groupdict().get('noncomment') is None and m.end() > m.start():
                tokens.append(Token(TokenType.COMMENT, m.group(), m.start(), m.end(),
                                    _line_at(newlines, m.start())))
        return tokens

    @classmethod
    def extract_comments(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_comments(source)]

    @classmethod
    def count_comments(cls, source: str) -> int:
        return len(cls.match_comments(source))

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> Union[str, List[str]]:
        """Strip comments using the language's comment_regex.

        The regex is expected to provide a 'noncomment' named group for text to keep.
        Returns either the joined string or a list of non-comment segments when isList=True.
        """
        result = []
        for match in cls.comment_regex().finditer(source_code):
            non = match.groupdict().get('noncomment')
            if non is not None:
                result.append(non)
        if isList:
            return result
        return ''.join(result)

    # ----------------------------------------------------------------- keywords
    @classmethod
    def match_keywords(cls, source: str) -> List[Token]:
        if not [w for w in (cls.keywords() or []) if w]:
            return []
        return cls._match_spans(cls.keywords_regex(), source, TokenType.KEYWORD)

    @classmethod
    def extract_keywords(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_keywords(source)]

    @classmethod
    def count_keywords(cls, source: str) -> int:
        return len(cls.match_keywords(source))

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)

    # ------------------------------------------------------------------ numbers
    @classmethod
    def match_numbers(cls, source: str) -> List[Token]:
        return cls._match_spans(cls.number_regex(), source, TokenType.NUMBER)

    @classmethod
    def extract_numbers(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_numbers(source)]

    @classmethod
    def count_numbers(cls, source: str) -> int:
        return len(cls.match_numbers(source))

    @classmethod
    def remove_numbers(cls, source: str) -> str:
        return re.sub(cls.number_regex(), '', source)

    # ---------------------------------------------------------------- operators
    @classmethod
    def match_operators(cls, source: str) -> List[Token]:
        return cls._match_spans(cls.operator_regex(), source, TokenType.OPERATOR)

    @classmethod
    def extract_operators(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_operators(source)]

    @classmethod
    def count_operators(cls, source: str) -> int:
        return len(cls.match_operators(source))

    @classmethod
    def remove_operators(cls, source: str) -> str:
        return re.sub(cls.operator_regex(), '', source)

    # ------------------------------------------------------------------ strings
    @classmethod
    def match_strings(cls, source: str) -> List[Token]:
        return cls._match_spans(cls.string_regex(), source, TokenType.STRING)

    @classmethod
    def extract_strings(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_strings(source)]

    @classmethod
    def count_strings(cls, source: str) -> int:
        return len(cls.match_strings(source))

    @classmethod
    def remove_strings(cls, source: str) -> str:
        return re.sub(cls.string_regex(), '', source)

    # -------------------------------------------------------------- identifiers
    @classmethod
    def match_identifiers(cls, source: str) -> List[Token]:
        """Match identifiers (words that are not language keywords)."""
        kws = {w.lower() for w in (cls.keywords() or []) if w}
        newlines = _newline_offsets(source)
        tokens = []
        for m in cls.identifier_regex().finditer(source):
            if m.group().lower() in kws:
                continue
            tokens.append(Token(TokenType.IDENTIFIER, m.group(), m.start(), m.end(),
                                _line_at(newlines, m.start())))
        return tokens

    @classmethod
    def extract_identifiers(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_identifiers(source)]

    @classmethod
    def count_identifiers(cls, source: str) -> int:
        return len(cls.match_identifiers(source))

    # ----------------------------------------------------------------- tokenize
    @classmethod
    def tokenize(cls, source: str) -> List[Token]:
        """Split ``source`` into a flat list of typed :class:`Token`s.

        Comments (and strings, where the language's ``comment_regex`` keeps them in
        the non-comment group) are separated first; remaining code is classified
        into strings, numbers, keywords, identifiers, operators and other
        single-character tokens. This is best-effort and driven by the language's
        own regexes.
        """
        newlines = _newline_offsets(source)
        tokens = []
        pos = 0
        for m in cls.comment_regex().finditer(source):
            if m.start() > pos:
                # Characters the comment regex does not classify (often newlines);
                # tokenize them as code so nothing is lost.
                cls._tokenize_code(source[pos:m.start()], pos, newlines, tokens)
                pos = m.start()
            if m.end() <= m.start():
                continue
            if m.groupdict().get('noncomment') is None:
                tokens.append(Token(TokenType.COMMENT, m.group(), m.start(), m.end(),
                                    _line_at(newlines, m.start())))
            else:
                cls._tokenize_code(m.group('noncomment'), m.start(), newlines, tokens)
            pos = m.end()
        if pos < len(source):
            cls._tokenize_code(source[pos:], pos, newlines, tokens)
        return tokens

    @classmethod
    def _tokenize_code(cls, text: str, base: int, newlines: List[int],
                       tokens: List[Token]) -> None:
        strx = cls.string_regex()
        numx = cls.number_regex()
        idx = cls.identifier_regex()
        kws = {w.lower() for w in (cls.keywords() or []) if w}
        stages = (
            (_WHITESPACE_RE, TokenType.WHITESPACE),
            (strx, TokenType.STRING),
            (numx, TokenType.NUMBER),
            (idx, None),  # identifier or keyword
            (_OPERATOR_RE, TokenType.OPERATOR),
        )
        i, n = 0, len(text)
        while i < n:
            for regex, ttype in stages:
                m = regex.match(text, i)
                if m and m.end() > i:
                    val = m.group()
                    if ttype is None:
                        tt = TokenType.KEYWORD if val.lower() in kws else TokenType.IDENTIFIER
                    else:
                        tt = ttype
                    start = base + i
                    tokens.append(Token(tt, val, start, start + len(val),
                                        _line_at(newlines, start)))
                    i = m.end()
                    break
            else:
                start = base + i
                tokens.append(Token(TokenType.OTHER, text[i], start, start + 1,
                                    _line_at(newlines, start)))
                i += 1

    # -------------------------------------------------------------- line-preserving
    @classmethod
    def blank_comments(cls, source: str, replacement: str = ' ') -> str:
        """Remove comment *content* while preserving line numbers.

        Each comment is replaced with ``replacement`` for every non-newline
        character and its newlines are kept, so downstream line/column mapping
        stays intact. Use ``replacement=''`` to blank only the content.
        """
        result = []
        pos = 0
        for tok in cls.match_comments(source):
            result.append(source[pos:tok.start])
            result.append(''.join('\n' if ch == '\n' else replacement for ch in tok.value))
            pos = tok.end
        result.append(source[pos:])
        return ''.join(result)

    # --------------------------------------------------------------------- metrics
    @classmethod
    def stats(cls, source: str) -> CodeStats:
        """Compute line- and token-level :class:`CodeStats` for ``source``."""
        from .. import _tokenops
        return _tokenops.stats(cls.tokenize(source), source)

    @classmethod
    def halstead(cls, source: str):
        """Return the :class:`~PyReprism.metrics.Halstead` measures for ``source``."""
        from .. import _tokenops
        return _tokenops.halstead(cls.tokenize(source))

    @classmethod
    def cyclomatic_complexity(cls, source: str) -> int:
        """Approximate McCabe cyclomatic complexity (token-based)."""
        from .. import _tokenops
        return _tokenops.cyclomatic(cls.tokenize(source))

    @classmethod
    def max_nesting_depth(cls, source: str) -> int:
        """Maximum bracket nesting depth."""
        from .. import _tokenops
        return _tokenops.max_nesting_depth(cls.tokenize(source))

    @classmethod
    def maintainability_index(cls, source: str) -> float:
        """SEI-normalized Maintainability Index in ``[0, 100]`` (higher is better)."""
        from .. import _tokenops
        tokens = cls.tokenize(source)
        return _tokenops.maintainability_index(tokens, _tokenops.stats(tokens, source).code_lines)

    @classmethod
    def code_metrics(cls, source: str) -> dict:
        """Return a combined metrics dict (line stats + Halstead + complexity + MI)."""
        from .. import _tokenops
        tokens = cls.tokenize(source)
        stats = _tokenops.stats(tokens, source)
        data = stats.as_dict()
        data['halstead'] = _tokenops.halstead(tokens).as_dict()
        data['cyclomatic_complexity'] = _tokenops.cyclomatic(tokens)
        data['max_nesting_depth'] = _tokenops.max_nesting_depth(tokens)
        data['maintainability_index'] = _tokenops.maintainability_index(tokens, stats.code_lines)
        return data

    # ------------------------------------------------------------------ normalize
    @classmethod
    def normalize(cls, source: str, **options) -> str:
        """Return a canonicalized form of ``source`` for ML / clone detection.

        By default: comments are dropped; string and number literals are replaced
        with fixed placeholders; and identifiers are consistently renamed to
        ``VAR1``, ``VAR2``, ... (keywords are preserved). Options mirror
        :func:`PyReprism._tokenops.normalize` (``rename_identifiers``,
        ``mask_numbers``, ``mask_strings``, ``drop_comments``,
        ``collapse_whitespace``, ``identifier_prefix``, ``number_placeholder``,
        ``string_placeholder``).
        """
        from .. import _tokenops
        return _tokenops.normalize(cls.tokenize(source), **options)
