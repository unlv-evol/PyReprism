"""A higher-accuracy backend powered by the optional Pygments dependency.

Pygments ships real lexers for every language PyReprism supports, so this engine
classifies comments, strings and other constructs far more reliably than the
regex fallback — at the cost of one extra dependency (``pip install
pyreprism[accurate]``).
"""
from typing import List

from ..tokens import Token, TokenType
from .base import Engine

# Language class name -> pygments lexer alias, only where they differ or the
# regex/name form is ambiguous. Everything else falls back to the lowercased
# class name and then to the file extension.
_ALIASES = {
    'CPP': 'cpp',
    'CSharp': 'csharp',
    'ObjectiveC': 'objective-c',
    'Clike': 'c',
    'MarkUp': 'html',
    'MarkupTemplating': 'html',
    'JavaScript': 'javascript',
    'TypeScript': 'typescript',
    'VisualBasic': 'vbnet',
    'Vbnet': 'vbnet',
    'MakeFile': 'make',
    'MarkDown': 'markdown',
}


class PygmentsEngine(Engine):
    """Tokenize using Pygments lexers, mapped onto PyReprism's token model."""

    name = 'pygments'

    def __init__(self):
        try:
            import pygments  # noqa: F401
        except ImportError as exc:  # pragma: no cover - exercised only without pygments
            raise ImportError(
                "the 'pygments' engine requires Pygments; install it with "
                "`pip install pyreprism[accurate]` (or `pip install pygments`)."
            ) from exc
        self._lexers = {}

    def _lexer(self, language_cls):
        from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
        from pygments.util import ClassNotFound

        name = language_cls.__name__
        if name in self._lexers:
            return self._lexers[name]
        alias = _ALIASES.get(name, name.lower())
        lexer = None
        try:
            lexer = get_lexer_by_name(alias)
        except ClassNotFound:
            try:
                ext = language_cls.file_extension()
                fname = ('file' + ext) if ext.startswith('.') else ext
                lexer = get_lexer_for_filename(fname)
            except ClassNotFound as exc:
                raise ValueError(
                    f"Pygments has no lexer for language {name!r}"
                ) from exc
        self._lexers[name] = lexer
        return lexer

    @staticmethod
    def _map(ttype, value: str) -> TokenType:
        from pygments.token import (Comment, Keyword, Name, Number, Operator,
                                    String, Whitespace)
        if ttype in Comment:
            return TokenType.COMMENT
        if ttype in String:
            return TokenType.STRING
        if ttype in Number:
            return TokenType.NUMBER
        if ttype in Keyword:
            return TokenType.KEYWORD
        if ttype in Name:
            return TokenType.IDENTIFIER
        if ttype in Operator:
            return TokenType.OPERATOR
        if ttype in Whitespace or value.isspace():
            return TokenType.WHITESPACE
        return TokenType.OTHER

    def tokenize(self, source: str, language_cls) -> List[Token]:
        lexer = self._lexer(language_cls)
        tokens = []
        # get_tokens_unprocessed is lossless and yields absolute offsets.
        # Pygments splits e.g. a string literal into quote/content/quote tokens;
        # coalesce consecutive tokens of the same kind so a whole comment or
        # string surfaces as one token (matching the regex engine's granularity).
        for index, ttype, value in lexer.get_tokens_unprocessed(source):
            if value == '':
                continue
            kind = self._map(ttype, value)
            if tokens and tokens[-1].type is kind and tokens[-1].end == index:
                prev = tokens[-1]
                tokens[-1] = Token(kind, prev.value + value, prev.start,
                                   index + len(value), prev.line)
            else:
                line = source.count('\n', 0, index) + 1
                tokens.append(Token(kind, value, index, index + len(value), line))
        return tokens
