"""PyReprism: a framework for source-code preprocessing.

High-level convenience API::

    import PyReprism as pr

    pr.remove_comments(src, lang="python")
    pr.extract_comments(src, lang="python")
    pr.count_comments(src, lang="python")
    pr.tokenize(src, lang="python")
    pr.preprocess(src, lang="java", steps=["comments", "strings", "whitespace"])

``lang`` may be a language name (``"python"``), a file extension (``".py"``), or a
language class. Use :func:`detect_language` to infer it from a filename.
"""
import importlib
import os
from typing import List, Optional, Sequence, Type, Union

from .metrics import CodeStats
from .tokens import Token, TokenType
from .utils.normalizer import Normalizer

__version__ = "0.1.0"

LanguageLike = Union[str, "type"]


def get_language(lang: LanguageLike) -> Type:
    """Resolve ``lang`` to a registered language class.

    Accepts a language class, a registry name (``"Python"``/``"python"``), or a
    file extension (``".py"``). Raises :class:`ValueError` if it cannot be resolved.
    """
    from .languages import _load_all_languages, get_language_by_extension
    from .languages.base import BaseLanguage
    from .languages.registry import LanguageRegistry

    if isinstance(lang, type) and issubclass(lang, BaseLanguage):
        return lang
    if isinstance(lang, str):
        name = lang.strip()
        cls = LanguageRegistry.get(name)
        if cls:
            return cls
        if name.startswith('.') or '.' in os.path.basename(name):
            cls = get_language_by_extension(name if name.startswith('.') else os.path.splitext(name)[1])
            if cls:
                return cls
        try:
            mod = importlib.import_module(f'.languages.{name.lower()}', __name__)
            for value in vars(mod).values():
                if (isinstance(value, type) and issubclass(value, BaseLanguage)
                        and value.__module__ == mod.__name__):
                    return value
        except ModuleNotFoundError:
            pass
        _load_all_languages()
        cls = (LanguageRegistry.get(name) or LanguageRegistry.get(name.capitalize())
               or LanguageRegistry.get(name.upper()))
        if cls:
            return cls
    raise ValueError(f"Unknown language: {lang!r}")


# Interpreter substrings found in a ``#!`` shebang -> registry class name.
_SHEBANG_LANGUAGES = [
    ('python', 'Python'), ('pypy', 'Python'),
    ('nodejs', 'JavaScript'), ('node', 'JavaScript'),
    ('ruby', 'Ruby'), ('perl', 'Perl'), ('php', 'PHP'),
    ('rscript', 'R'), ('groovy', 'Groovy'), ('lua', 'LUA'),
    ('tclsh', 'Tcl'), ('wish', 'Tcl'),
    ('bash', 'Bash'), ('zsh', 'Bash'), ('ksh', 'Bash'), ('/sh', 'Bash'),
]


def _detect_from_shebang(source: str) -> Optional[Type]:
    stripped = source.lstrip()
    first = stripped.splitlines()[0] if stripped else ''
    if not first.startswith('#!'):
        return None
    from .languages import _load_all_languages
    from .languages.registry import LanguageRegistry
    line = first.lower()
    for token, name in _SHEBANG_LANGUAGES:
        if token in line:
            _load_all_languages()
            cls = LanguageRegistry.get(name)
            if cls is not None:
                return cls
    return None


def _guess_with_pygments(source: str) -> Optional[Type]:
    try:
        from pygments.lexers import guess_lexer
        from pygments.util import ClassNotFound
    except ImportError:
        return None
    from .languages import get_language_by_extension
    try:
        lexer = guess_lexer(source)
    except ClassNotFound:
        return None
    for alias in getattr(lexer, 'aliases', []):
        try:
            return get_language(alias)
        except ValueError:
            continue
    for pattern in getattr(lexer, 'filenames', []):
        ext = os.path.splitext(pattern)[1]
        if ext:
            cls = get_language_by_extension(ext)
            if cls is not None:
                return cls
    return None


def detect_language(filename: Optional[str] = None, source: Optional[str] = None) -> Optional[Type]:
    """Infer a language class from a ``filename`` and/or a ``source`` string.

    Resolution order: filename extension, then (if ``source`` is given) a ``#!``
    shebang line, then a best-effort Pygments content guess when Pygments is
    installed. Returns ``None`` when nothing matches.
    """
    from .languages import get_language_by_extension

    if filename:
        base = os.path.basename(filename)
        _, ext = os.path.splitext(base)
        cls = get_language_by_extension(ext or base)
        if cls is not None:
            return cls
    if source:
        cls = _detect_from_shebang(source)
        if cls is not None:
            return cls
        return _guess_with_pygments(source)
    return None


# --------------------------------------------------------------------- helpers
def _resolve(lang: LanguageLike) -> Type:
    return get_language(lang)


_CONSTRUCT_TYPE = {
    'comments': TokenType.COMMENT, 'strings': TokenType.STRING,
    'numbers': TokenType.NUMBER, 'keywords': TokenType.KEYWORD,
    'operators': TokenType.OPERATOR, 'identifiers': TokenType.IDENTIFIER,
}


def _engine_tokens(source: str, lang: LanguageLike, engine: str) -> List[Token]:
    from .engines import get_engine
    return get_engine(engine).tokenize(source, _resolve(lang))


def _is_regex(engine) -> bool:
    return engine in (None, 'regex')


def _op(action: str, construct: str, source: str, lang: LanguageLike, engine: str):
    """Run remove/extract/count for a construct via the selected engine."""
    if _is_regex(engine):
        return getattr(_resolve(lang), f'{action}_{construct}')(source)
    from . import _tokenops
    tokens = _engine_tokens(source, lang, engine)
    return getattr(_tokenops, action)(tokens, _CONSTRUCT_TYPE[construct])


def remove_comments(source: str, lang: LanguageLike, engine: str = 'regex', isList: bool = False):
    """Remove comments from ``source`` for the given language."""
    if _is_regex(engine):
        return _resolve(lang).remove_comments(source, isList=isList)
    tokens = _engine_tokens(source, lang, engine)
    if isList:
        return [t.value for t in tokens if t.type is not TokenType.COMMENT]
    from . import _tokenops
    return _tokenops.remove(tokens, TokenType.COMMENT)


def extract_comments(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'comments', source, lang, engine)


def count_comments(source: str, lang: LanguageLike, engine: str = 'regex') -> int:
    return _op('count', 'comments', source, lang, engine)


def match_comments(source: str, lang: LanguageLike, engine: str = 'regex') -> List[Token]:
    if _is_regex(engine):
        return _resolve(lang).match_comments(source)
    return [t for t in _engine_tokens(source, lang, engine) if t.type is TokenType.COMMENT]


def remove_keywords(source: str, lang: LanguageLike, engine: str = 'regex') -> str:
    if _is_regex(engine):
        return _resolve(lang).remove_keywords(source)
    return _op('remove', 'keywords', source, lang, engine)


def extract_keywords(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'keywords', source, lang, engine)


def count_keywords(source: str, lang: LanguageLike, engine: str = 'regex') -> int:
    return _op('count', 'keywords', source, lang, engine)


def remove_numbers(source: str, lang: LanguageLike, engine: str = 'regex') -> str:
    return _op('remove', 'numbers', source, lang, engine)


def extract_numbers(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'numbers', source, lang, engine)


def count_numbers(source: str, lang: LanguageLike, engine: str = 'regex') -> int:
    return _op('count', 'numbers', source, lang, engine)


def remove_operators(source: str, lang: LanguageLike, engine: str = 'regex') -> str:
    return _op('remove', 'operators', source, lang, engine)


def extract_operators(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'operators', source, lang, engine)


def remove_strings(source: str, lang: LanguageLike, engine: str = 'regex') -> str:
    return _op('remove', 'strings', source, lang, engine)


def extract_strings(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'strings', source, lang, engine)


def extract_identifiers(source: str, lang: LanguageLike, engine: str = 'regex') -> List[str]:
    return _op('extract', 'identifiers', source, lang, engine)


def remove_whitespaces(source: str) -> str:
    """Collapse insignificant whitespace (language-independent)."""
    return Normalizer.remove_whitespaces(source)


def tokenize(source: str, lang: LanguageLike, engine: str = 'regex') -> List[Token]:
    """Return the flat list of typed tokens for ``source``."""
    if _is_regex(engine):
        return _resolve(lang).tokenize(source)
    return _engine_tokens(source, lang, engine)


def blank_comments(source: str, lang: LanguageLike, replacement: str = ' ',
                   engine: str = 'regex') -> str:
    """Remove comment content while preserving line numbers."""
    if _is_regex(engine):
        return _resolve(lang).blank_comments(source, replacement=replacement)
    parts = []
    for tok in _engine_tokens(source, lang, engine):
        if tok.type is TokenType.COMMENT:
            parts.append(''.join('\n' if ch == '\n' else replacement for ch in tok.value))
        else:
            parts.append(tok.value)
    return ''.join(parts)


def stats(source: str, lang: LanguageLike, engine: str = 'regex') -> CodeStats:
    """Return line- and token-level :class:`CodeStats` for ``source``."""
    if _is_regex(engine):
        return _resolve(lang).stats(source)
    from . import _tokenops
    return _tokenops.stats(_engine_tokens(source, lang, engine), source)


def normalize(source: str, lang: LanguageLike, engine: str = 'regex', **options) -> str:
    """Return a canonicalized form of ``source`` for ML / clone detection.

    See :meth:`PyReprism.languages.base.BaseLanguage.normalize` for options.
    """
    if _is_regex(engine):
        return _resolve(lang).normalize(source, **options)
    from . import _tokenops
    return _tokenops.normalize(_engine_tokens(source, lang, engine), **options)


_STEPS = {
    'comments': lambda cls, s: cls.remove_comments(s),
    'strings': lambda cls, s: cls.remove_strings(s),
    'numbers': lambda cls, s: cls.remove_numbers(s),
    'operators': lambda cls, s: cls.remove_operators(s),
    'keywords': lambda cls, s: cls.remove_keywords(s),
    'whitespace': lambda cls, s: Normalizer.remove_whitespaces(s),
}


def preprocess(source: str, lang: LanguageLike, steps: Sequence[str] = ('comments',),
               engine: str = 'regex') -> str:
    """Apply a sequence of removal ``steps`` in order and return the result.

    Valid steps: ``comments``, ``strings``, ``numbers``, ``operators``,
    ``keywords``, ``whitespace``.
    """
    if steps is None:
        steps = ('comments',)
    if _is_regex(engine):
        cls = _resolve(lang)
        out = source
        for step in steps:
            fn = _STEPS.get(step)
            if fn is None:
                raise ValueError(f"Unknown preprocessing step: {step!r}. "
                                 f"Valid steps: {', '.join(sorted(_STEPS))}")
            out = fn(cls, out)
        return out
    from . import _tokenops
    out = source
    for step in steps:
        if step == 'whitespace':
            out = Normalizer.remove_whitespaces(out)
        elif step in _CONSTRUCT_TYPE:
            out = _tokenops.remove(_engine_tokens(out, lang, engine), _CONSTRUCT_TYPE[step])
        else:
            raise ValueError(f"Unknown preprocessing step: {step!r}. "
                             f"Valid steps: {', '.join(sorted(_STEPS))}")
    return out


__all__ = [
    '__version__',
    'Token', 'TokenType', 'CodeStats', 'Normalizer',
    'get_language', 'detect_language',
    'remove_comments', 'extract_comments', 'count_comments', 'match_comments',
    'remove_keywords', 'extract_keywords', 'count_keywords',
    'remove_numbers', 'extract_numbers', 'count_numbers',
    'remove_operators', 'extract_operators',
    'remove_strings', 'extract_strings',
    'extract_identifiers', 'remove_whitespaces',
    'blank_comments', 'stats', 'normalize',
    'tokenize', 'preprocess',
]
