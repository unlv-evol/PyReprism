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


_ALL_LOADED = False


def _load_all_languages() -> None:
    """Import every language submodule so the registry is fully populated.

    Language modules register themselves on import; without importing them the
    registry only knows about classes that have already been accessed. The
    package is scanned once per process.
    """
    global _ALL_LOADED
    if _ALL_LOADED:
        return
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
    _ALL_LOADED = True


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
    # '.v' is shared by Verilog and V (vlang); Verilog is far more common in
    # existing corpora, so it wins extension lookup. Resolve V by name (`v`).
    '.v': 'Verilog',
}


# Secondary extensions of languages whose module declares another one. Only
# extensions with the same lexical syntax are listed.
_EXTRA_EXTENSIONS = {
    '.h': 'C',
    '.cc': 'CPP', '.cxx': 'CPP', '.c++': 'CPP', '.hpp': 'CPP', '.hh': 'CPP',
    '.hxx': 'CPP', '.h++': 'CPP',
    '.mjs': 'JavaScript', '.cjs': 'JavaScript',
    '.mts': 'TypeScript', '.cts': 'TypeScript',
    '.pyi': 'Python', '.pyw': 'Python',
    '.bash': 'Bash', '.ksh': 'Bash', '.zsh': 'Bash',
    '.yml': 'Yaml', '.markdown': 'MarkDown', '.htm': 'HTML',
    '.kts': 'Kotlin', '.rake': 'Ruby', '.gemspec': 'Ruby', '.exs': 'Elixir',
    '.mli': 'Ocaml', '.fsx': 'FSharp', '.fsi': 'FSharp',
    '.cljs': 'Clojure', '.cljc': 'Clojure', '.psm1': 'PowerShell',
    '.psd1': 'PowerShell', '.pm': 'Perl', '.mm': 'ObjectiveC',
    '.gradle': 'Groovy', '.mk': 'MakeFile', '.sc': 'Scala',
}

_EXT_INDEX: dict = {}
_EXT_INDEX_SIZE = -1


def _extension_index() -> dict:
    """``{extension: class}``, rebuilt only when the registry grows."""
    global _EXT_INDEX, _EXT_INDEX_SIZE
    _load_all_languages()
    registry = LanguageRegistry.all()
    if len(registry) == _EXT_INDEX_SIZE:
        return _EXT_INDEX
    index: dict = {}
    for cls in registry.values():  # first registered match wins
        try:
            index.setdefault(cls.file_extension(), cls)
        except Exception:
            continue
    for ext, name in _PREFERRED_LANGUAGE.items():
        cls = registry.get(name)
        try:
            if cls is not None and cls.file_extension() == ext:
                index[ext] = cls
        except Exception:
            pass
    for ext, name in _EXTRA_EXTENSIONS.items():
        if ext not in index and registry.get(name) is not None:
            index[ext] = registry[name]
    _EXT_INDEX, _EXT_INDEX_SIZE = index, len(registry)
    return index


def get_language_by_extension(ext: str) -> Optional[Type[BaseLanguage]]:
    """Return a registered language class whose ``file_extension()`` matches ``ext``.

    All language modules are imported on first call so cold lookups succeed. Some
    extensions are shared by several languages (``.py`` -> Python/Django, ``.m`` ->
    MatLab/ObjectiveC); a small preference table picks the canonical language for the
    common cases, otherwise the first registered match is returned. Common
    secondary extensions (``.h``, ``.hpp``, ``.yml``, ...) map to their language.
    """
    return _extension_index().get(ext)
