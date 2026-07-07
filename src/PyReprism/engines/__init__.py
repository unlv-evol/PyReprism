"""Tokenization backends.

``regex`` (default) is zero-dependency and uses each language's own regexes.
``pygments`` is more accurate but needs the optional Pygments dependency.
``auto`` uses pygments when it is importable, otherwise falls back to regex.
"""
from .base import Engine
from .pygments_engine import PygmentsEngine
from .regex_engine import RegexEngine

_CACHE = {}


def get_engine(name: str = 'regex') -> Engine:
    """Return an :class:`Engine` instance for ``name`` (``regex``/``pygments``/``auto``)."""
    key = (name or 'regex').lower()
    if key in _CACHE:
        return _CACHE[key]
    if key == 'regex':
        engine = RegexEngine()
    elif key == 'pygments':
        engine = PygmentsEngine()
    elif key == 'auto':
        try:
            engine = PygmentsEngine()
        except ImportError:
            engine = RegexEngine()
    else:
        raise ValueError(f"Unknown engine: {name!r} (use 'regex', 'pygments' or 'auto')")
    _CACHE[key] = engine
    return engine


__all__ = ['Engine', 'RegexEngine', 'PygmentsEngine', 'get_engine']
