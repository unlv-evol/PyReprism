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

__version__ = "0.0.4"

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


def detect_language(filename: Optional[str] = None, source: Optional[str] = None) -> Optional[Type]:
    """Infer a language class from ``filename`` (by extension or basename).

    ``source``-based detection is not yet implemented and is accepted for
    forward compatibility. Returns ``None`` when no language matches.
    """
    from .languages import get_language_by_extension

    if filename:
        base = os.path.basename(filename)
        _, ext = os.path.splitext(base)
        return get_language_by_extension(ext or base)
    return None


# --------------------------------------------------------------------- helpers
def _resolve(lang: LanguageLike) -> Type:
    return get_language(lang)


def remove_comments(source: str, lang: LanguageLike, isList: bool = False):
    """Remove comments from ``source`` for the given language."""
    return _resolve(lang).remove_comments(source, isList=isList)


def extract_comments(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_comments(source)


def count_comments(source: str, lang: LanguageLike) -> int:
    return _resolve(lang).count_comments(source)


def match_comments(source: str, lang: LanguageLike) -> List[Token]:
    return _resolve(lang).match_comments(source)


def remove_keywords(source: str, lang: LanguageLike) -> str:
    return _resolve(lang).remove_keywords(source)


def extract_keywords(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_keywords(source)


def count_keywords(source: str, lang: LanguageLike) -> int:
    return _resolve(lang).count_keywords(source)


def remove_numbers(source: str, lang: LanguageLike) -> str:
    return _resolve(lang).remove_numbers(source)


def extract_numbers(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_numbers(source)


def count_numbers(source: str, lang: LanguageLike) -> int:
    return _resolve(lang).count_numbers(source)


def remove_operators(source: str, lang: LanguageLike) -> str:
    return _resolve(lang).remove_operators(source)


def extract_operators(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_operators(source)


def remove_strings(source: str, lang: LanguageLike) -> str:
    return _resolve(lang).remove_strings(source)


def extract_strings(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_strings(source)


def extract_identifiers(source: str, lang: LanguageLike) -> List[str]:
    return _resolve(lang).extract_identifiers(source)


def remove_whitespaces(source: str) -> str:
    """Collapse insignificant whitespace (language-independent)."""
    return Normalizer.remove_whitespaces(source)


def tokenize(source: str, lang: LanguageLike) -> List[Token]:
    """Return the flat list of typed tokens for ``source``."""
    return _resolve(lang).tokenize(source)


def blank_comments(source: str, lang: LanguageLike, replacement: str = ' ') -> str:
    """Remove comment content while preserving line numbers."""
    return _resolve(lang).blank_comments(source, replacement=replacement)


def stats(source: str, lang: LanguageLike) -> CodeStats:
    """Return line- and token-level :class:`CodeStats` for ``source``."""
    return _resolve(lang).stats(source)


def normalize(source: str, lang: LanguageLike, **options) -> str:
    """Return a canonicalized form of ``source`` for ML / clone detection.

    See :meth:`PyReprism.languages.base.BaseLanguage.normalize` for options.
    """
    return _resolve(lang).normalize(source, **options)


_STEPS = {
    'comments': lambda cls, s: cls.remove_comments(s),
    'strings': lambda cls, s: cls.remove_strings(s),
    'numbers': lambda cls, s: cls.remove_numbers(s),
    'operators': lambda cls, s: cls.remove_operators(s),
    'keywords': lambda cls, s: cls.remove_keywords(s),
    'whitespace': lambda cls, s: Normalizer.remove_whitespaces(s),
}


def preprocess(source: str, lang: LanguageLike, steps: Sequence[str] = ('comments',)) -> str:
    """Apply a sequence of removal ``steps`` in order and return the result.

    Valid steps: ``comments``, ``strings``, ``numbers``, ``operators``,
    ``keywords``, ``whitespace``.
    """
    cls = _resolve(lang)
    out = source
    for step in steps:
        fn = _STEPS.get(step)
        if fn is None:
            raise ValueError(f"Unknown preprocessing step: {step!r}. "
                             f"Valid steps: {', '.join(sorted(_STEPS))}")
        out = fn(cls, out)
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
