"""Long-tail language fallback backed by Pygments.

The 145 first-class languages are hand-written, zero-dependency regex modules and
remain the default. When a caller asks for a language or extension that is *not*
in the registry (say ``.zig`` or ``"solidity"``), and Pygments is installed, this
module builds a lightweight :class:`~PyReprism.languages.base.BaseLanguage`
subclass on the fly that delegates tokenization and comment handling to the
matching Pygments lexer. Pygments ships 500+ lexers, so this extends coverage far
beyond the built-in set without a per-language module.

Fallback languages are deliberately **not** added to
:class:`~PyReprism.languages.registry.LanguageRegistry`: they are resolved on
demand, they are not validated against the per-language comment test suite, and
they should be treated as *supported* (best-effort) rather than *validated*.
Keyword-level operations are limited (the lexer classifies keywords in the token
stream, but ``keywords()`` is empty, so ``remove_keywords`` is a no-op).
"""
from functools import lru_cache
from typing import List, Optional, Type

from ..tokens import Token, TokenType
from .base import BaseLanguage


def _first_extension(lexer) -> str:
    """Best-effort file extension from a Pygments lexer's filename globs."""
    for pattern in getattr(lexer, 'filenames', []) or []:
        if pattern.startswith('*.'):
            return pattern[1:]  # '*.zig' -> '.zig'
    return ''


def _tokenize_with_lexer(source: str, lexer) -> List[Token]:
    """Lossless token stream from a Pygments lexer, coalescing adjacent same-kind
    tokens so a whole comment/string surfaces as one token (matching the regex
    engine's granularity). Mirrors ``PygmentsEngine.tokenize``."""
    from ..engines.pygments_engine import PygmentsEngine
    tokens: List[Token] = []
    for index, ttype, value in lexer.get_tokens_unprocessed(source):
        if value == '':
            continue
        kind = PygmentsEngine._map(ttype, value)
        if tokens and tokens[-1].type is kind and tokens[-1].end == index:
            prev = tokens[-1]
            tokens[-1] = Token(kind, prev.value + value, prev.start,
                               index + len(value), prev.line)
        else:
            line = source.count('\n', 0, index) + 1
            tokens.append(Token(kind, value, index, index + len(value), line))
    return tokens


def _is_non_language_lexer(lexer) -> bool:
    """True for Pygments' generic fallback lexers (plain text / raw tokens), which
    are not real languages and must not masquerade as a detected language."""
    try:
        from pygments.lexers.special import RawTokenLexer, TextLexer
        if isinstance(lexer, (TextLexer, RawTokenLexer)):
            return True
    except ImportError:
        pass
    return False


def _resolve_lexer(spec: str):
    """Return a Pygments lexer for a language name or ``.ext``, or ``None``."""
    try:
        from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
        from pygments.util import ClassNotFound
    except ImportError:
        return None
    spec = (spec or '').strip()
    if not spec:
        return None
    lexer = None
    if spec.startswith('.'):
        try:
            lexer = get_lexer_for_filename('file' + spec)
        except ClassNotFound:
            return None
    else:
        try:
            lexer = get_lexer_by_name(spec.lower())
        except ClassNotFound:
            # A bare filename like "build.zig" or an extension without a dot.
            try:
                lexer = get_lexer_for_filename(spec if '.' in spec else 'file.' + spec)
            except ClassNotFound:
                return None
    if lexer is None or _is_non_language_lexer(lexer):
        return None
    return lexer


@lru_cache(maxsize=None)
def pygments_language_for(spec: str) -> Optional[Type[BaseLanguage]]:
    """Build (and cache) a Pygments-backed language class for ``spec``.

    ``spec`` is a language name (``"zig"``) or a file extension (``".zig"``).
    Returns ``None`` when Pygments is not installed or has no matching lexer, so
    callers can fall through to their existing error handling.
    """
    lexer = _resolve_lexer(spec)
    if lexer is None:
        return None

    ext = spec if spec.startswith('.') else _first_extension(lexer)
    display = (lexer.aliases[0] if getattr(lexer, 'aliases', None) else spec.lower())
    class_name = 'Pygments_' + ''.join(ch if ch.isalnum() else '_' for ch in display)

    def file_extension(cls) -> str:
        return ext

    def keywords(cls) -> list:
        return []

    def tokenize(cls, source: str) -> List[Token]:
        return _tokenize_with_lexer(source, lexer)

    def match_comments(cls, source: str) -> List[Token]:
        return [t for t in cls.tokenize(source) if t.type is TokenType.COMMENT]

    def extract_comments(cls, source: str) -> List[str]:
        return [t.value for t in cls.match_comments(source)]

    def count_comments(cls, source: str) -> int:
        return len(cls.match_comments(source))

    def remove_comments(cls, source_code: str, isList: bool = False):
        segs = [t.value for t in cls.tokenize(source_code)
                if t.type is not TokenType.COMMENT]
        return segs if isList else ''.join(segs)

    def comment_regex(cls):
        raise NotImplementedError(
            f"{class_name} is Pygments-backed and has no regex comment pattern; "
            "use tokenize()/remove_comments() instead."
        )

    namespace = {
        '__doc__': f"Pygments-backed fallback language for {display!r} "
                   f"(lexer: {lexer.name}). Supported, not validated.",
        'pygments_backed': True,
        'file_extension': classmethod(file_extension),
        'keywords': classmethod(keywords),
        'tokenize': classmethod(tokenize),
        'match_comments': classmethod(match_comments),
        'extract_comments': classmethod(extract_comments),
        'count_comments': classmethod(count_comments),
        'remove_comments': classmethod(remove_comments),
        'comment_regex': classmethod(comment_regex),
    }
    return type(class_name, (BaseLanguage,), namespace)
