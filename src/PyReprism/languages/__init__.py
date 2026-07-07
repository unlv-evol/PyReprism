"""Language registry bridge and lazy loader for PyReprism language modules.

Each language lives in ``PyReprism/languages/<name>.py`` and self-registers with
:class:`~PyReprism.languages.registry.LanguageRegistry` on import. Language classes
can be accessed lazily as attributes, e.g. ``PyReprism.languages.Python``.
"""
import importlib
import os
import pkgutil
from typing import Any, Optional, Type

from .. import __version__  # single source of truth for the package version
from .base import BaseLanguage
from .registry import LanguageRegistry

# Common languages surfaced for discoverability. Any registered language is
# importable by name regardless of whether it appears here (see ``__getattr__``).
__all__ = [
    'Python', 'JavaScript', 'CPP', 'C', 'Clike', 'Go', 'MatLab', 'Ruby', 'PHP', 'Bash',
    'get_language_by_extension',
]


def __getattr__(name: str) -> Any:
    """Lazy-load a language class by attribute name.

    Accessing e.g. ``PyReprism.languages.Python`` imports the submodule
    ``PyReprism.languages.python`` and returns the registered class.
    """
    cls = LanguageRegistry.get(name)
    if cls:
        return cls

    try:
        importlib.import_module(f'.{name.lower()}', __name__)
    except ModuleNotFoundError:
        raise AttributeError(f"module {__name__} has no attribute {name}")

    cls = LanguageRegistry.get(name)
    if cls:
        return cls
    raise AttributeError(f"module {__name__} has no attribute {name}")


def _load_all_languages() -> None:
    """Import every language submodule so the registry is fully populated.

    Language modules register themselves on import; without importing them the
    registry only knows about classes that have already been accessed.
    """
    package_dir = os.path.dirname(__file__)
    for module in pkgutil.iter_modules([package_dir]):
        name = module.name
        if name.startswith('_') or name in ('base', 'registry'):
            continue
        try:
            importlib.import_module(f'.{name}', __name__)
        except Exception:
            # A broken/optional language module should not break lookups.
            continue


# For extensions shared by several languages, prefer the canonical/primary one.
_PREFERRED_LANGUAGE = {
    '.py': 'Python',
    '.h': 'C',
    '.r': 'R',
    '.pl': 'Perl',
    '.ts': 'TypeScript',
    '.php': 'PHP',
    '.sql': 'SQL',
    '.vb': 'Vbnet',
    '.js': 'JavaScript',
}


def get_language_by_extension(ext: str) -> Optional[Type[BaseLanguage]]:
    """Return a registered language class whose ``file_extension()`` matches ``ext``.

    All language modules are imported on first call so cold lookups succeed. Some
    extensions are shared by several languages (``.py`` -> Python/Django, ``.m`` ->
    MatLab/ObjectiveC); a small preference table picks the canonical language for the
    common cases, otherwise the first registered match is returned.
    """
    _load_all_languages()
    registry = LanguageRegistry.all()
    preferred = _PREFERRED_LANGUAGE.get(ext)
    if preferred:
        cls = registry.get(preferred)
        try:
            if cls is not None and cls.file_extension() == ext:
                return cls
        except Exception:
            pass
    for cls in registry.values():
        try:
            if cls.file_extension() == ext:
                return cls
        except Exception:
            continue
    return None
