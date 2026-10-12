import bisect
import re
from functools import lru_cache
from typing import List, Pattern, Union

from ..metrics import CodeStats
from ..tokens import Token, TokenType

# Shared, language-agnostic patterns used by the generic tokenizer.
# A byte-order mark (U+FEFF) at the start of a file is whitespace, not code.
_WHITESPACE_RE = re.compile(r'[\s\ufeff]+')
_OPERATOR_RE = re.compile(r'[-+*/%=<>!&|^~?]+')


_NEWLINE_RE = re.compile('\n')
_new_token = tuple.__new__  # Token(...) without the NamedTuple call overhead


def _newline_offsets(source: str) -> List[int]:
    return [m.start() for m in _NEWLINE_RE.finditer(source)]


# Scoped inline flags (``(?i:...)``) let one combined pattern keep each
# stage's own flags.
_SCOPED_FLAGS = ((re.IGNORECASE, 'i'), (re.MULTILINE, 'm'), (re.DOTALL, 's'),
                 (re.VERBOSE, 'x'), (re.ASCII, 'a'))
_ANY_RE = re.compile(r'.', re.DOTALL)
# Backreferences would point at the wrong groups once joined, and global
# inline flags such as ``(?i)`` would apply to the whole joined pattern.
_UNJOINABLE_RE = re.compile(r'\\[1-9]|\(\?P=|\(\?[aiLmsux]+\)')


class _CodeLexer:
    """The per-language plan for :meth:`BaseLanguage._tokenize_code`.

    The stages (whitespace, string, number, identifier/keyword, operator) are
    tried in order at each position, and the first non-empty match wins. Where
    possible they are joined into one alternation, which the regex engine tries
    in the same order, so each token costs one match instead of up to five.
    Patterns with backreferences or global inline flags cannot be joined;
    those languages, and any position where the joined pattern matches the
    empty string, use the stage-by-stage loop.
    """

    __slots__ = ('stages', 'keywords', 'combined', 'kinds')

    def __init__(self, cls):
        self.keywords = frozenset(w.lower() for w in (cls.keywords() or []) if w)
        self.stages = (
            (_WHITESPACE_RE, TokenType.WHITESPACE),
            (cls.string_regex(), TokenType.STRING),
            (cls.number_regex(), TokenType.NUMBER),
            (cls.identifier_regex(), None),  # identifier or keyword
            (_OPERATOR_RE, TokenType.OPERATOR),
        )
        self.combined, self.kinds = None, None
        parts, kinds, group = [], {}, 1
        for regex, ttype in self.stages + ((_ANY_RE, TokenType.OTHER),):
            if _UNJOINABLE_RE.search(regex.pattern):
                return
            flags = ''.join(c for f, c in _SCOPED_FLAGS if regex.flags & f)
            parts.append(f'((?{flags}:{regex.pattern}))')
            kinds[group] = ttype  # each stage is one outer group
            group += 1 + regex.groups
        try:
            self.combined = re.compile('|'.join(parts))
        except re.error:
            return
        self.kinds = kinds


_LEXERS = {}


def _code_lexer(cls) -> _CodeLexer:
    lexer = _LEXERS.get(cls)
    if lexer is None:
        lexer = _LEXERS[cls] = _CodeLexer(cls)
    return lexer


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
        pos = 0
        for match in cls.comment_regex().finditer(source_code):
            if match.start() > pos:
                # Text the regex skipped is code, as in tokenize(); dropping it
                # would delete characters such as a '/' inside a string.
                result.append(source_code[pos:match.start()])
            non = match.groupdict().get('noncomment')
            if non is not None:
                result.append(non)
            pos = max(pos, match.end())
        if pos < len(source_code):
            result.append(source_code[pos:])
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
            try:
                non = m.group('noncomment')
            except IndexError:  # a regex without a 'noncomment' group
                non = None
            if non is None:
                tokens.append(_new_token(Token, (TokenType.COMMENT, m.group(), m.start(),
                                                 m.end(), _line_at(newlines, m.start()))))
            else:
                cls._tokenize_code(non, m.start(), newlines, tokens)
            pos = m.end()
        if pos < len(source):
            cls._tokenize_code(source[pos:], pos, newlines, tokens)
        return tokens

    @classmethod
    def _tokenize_code(cls, text: str, base: int, newlines: List[int],
                       tokens: List[Token]) -> None:
        if not text:
            return
        lexer = _code_lexer(cls)
        kws, kinds = lexer.keywords, lexer.kinds
        append = tokens.append
        keyword, identifier = TokenType.KEYWORD, TokenType.IDENTIFIER
        # Line of position ``base`` (newlines strictly before it). Tokens that
        # start on a newline get the next line, matching _line_at().
        line = bisect.bisect_left(newlines, base) + 1
        i = 0
        if lexer.combined is not None:
            # The last alternative matches any character, so matches are
            # contiguous: each token starts where the previous one ended.
            for m in lexer.combined.finditer(text):
                end = m.end()
                if end == i:
                    break  # a stage matched the empty string: go stage by stage
                val = m.group()
                tt = kinds[m.lastindex]
                if tt is None:
                    tt = keyword if val.lower() in kws else identifier
                breaks = val.count('\n')
                append(_new_token(Token, (tt, val, base + i, base + end,
                                          line + 1 if breaks and val[0] == '\n' else line)))
                line += breaks
                i = end
            else:
                return
        n = len(text)
        while i < n:
            for regex, ttype in lexer.stages:
                m = regex.match(text, i)
                if m and m.end() > i:
                    val = m.group()
                    if ttype is None:
                        tt = keyword if val.lower() in kws else identifier
                    else:
                        tt = ttype
                    break
            else:
                val, tt = text[i], TokenType.OTHER
            start = base + i
            breaks = val.count('\n')
            append(_new_token(Token, (tt, val, start, start + len(val),
                                      line + 1 if breaks and val[0] == '\n' else line)))
            line += breaks
            i += len(val)

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
        result = cls._counted_stats(source)
        if result is None:
            from .. import _tokenops
            result = _tokenops.stats(cls.tokenize(source), source)
        return result

    @classmethod
    def _counted_stats(cls, source: str):
        """:meth:`stats` without building the token list.

        Runs the same passes as :meth:`tokenize` but counts each token as it is
        classified. Returns ``None`` (the caller then uses the token list) when
        the language tokenizes differently or the joined code pattern cannot be
        used, so the result always equals ``_tokenops.stats(tokenize(source))``.
        """
        if (cls.tokenize.__func__ is not BaseLanguage.tokenize.__func__
                or cls._tokenize_code.__func__ is not BaseLanguage._tokenize_code.__func__):
            return None
        lexer = _code_lexer(cls)
        combined = lexer.combined
        if combined is None:
            return None
        kws, kinds = lexer.keywords, lexer.kinds
        counts = dict.fromkeys(TokenType, 0)
        whitespace, keyword, identifier = (TokenType.WHITESPACE, TokenType.KEYWORD,
                                           TokenType.IDENTIFIER)
        code_lines, comment_lines = set(), set()
        newlines = _newline_offsets(source)

        def code(text, base):  # mirrors the joined-pattern loop of _tokenize_code
            line = bisect.bisect_left(newlines, base) + 1
            i = 0
            for m in combined.finditer(text):
                end = m.end()
                if end == i:
                    return False
                tt = kinds[m.lastindex]
                if tt is None:
                    tt = keyword if m.group().lower() in kws else identifier
                counts[tt] += 1
                breaks = text.count('\n', i, end)
                if tt is not whitespace:
                    if breaks:
                        code_lines.update(range(line, line + breaks + 1))
                    else:
                        code_lines.add(line)
                line += breaks
                i = end
            return True

        pos = 0
        for m in cls.comment_regex().finditer(source):
            start, end = m.start(), m.end()
            if start > pos:
                if not code(source[pos:start], pos):
                    return None
                pos = start
            if end <= start:
                continue
            try:
                non = m.group('noncomment')
            except IndexError:
                non = None
            if non is None:
                counts[TokenType.COMMENT] += 1
                line = _line_at(newlines, start)
                comment_lines.update(range(line, line + source.count('\n', start, end) + 1))
            elif not code(non, start):
                return None
            pos = end
        if pos < len(source) and not code(source[pos:], pos):
            return None
        total = len(source.splitlines())
        n_code = len(code_lines)
        n_comment = len(comment_lines - code_lines)
        return CodeStats(
            lines=total, code_lines=n_code, comment_lines=n_comment,
            blank_lines=max(total - n_code - n_comment, 0), characters=len(source),
            comment_tokens=counts[TokenType.COMMENT], string_tokens=counts[TokenType.STRING],
            number_tokens=counts[TokenType.NUMBER], keyword_tokens=counts[keyword],
            identifier_tokens=counts[identifier], operator_tokens=counts[TokenType.OPERATOR],
        )

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
        return _tokenops.code_metrics(cls.tokenize(source), source)

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
