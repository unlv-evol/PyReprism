from typing import Dict, Type

from .base import BaseLanguage


class LanguageRegistry:
    _registry: Dict[str, Type[BaseLanguage]] = {}

    @classmethod
    def register(cls, language_cls: Type[BaseLanguage]):
        cls._registry[language_cls.__name__] = language_cls
        return language_cls

    @classmethod
    def get(cls, name: str):
        # If not registered yet, try lazy-importing the module by lowercase name
        if name not in cls._registry:
            try:
                import importlib
                # Try importing using this module's package first. On case-insensitive
                # filesystems the package may be imported with different capitalization
                # (e.g. PyRePrism vs PyReprism). Attempt the package recorded in
                # __package__, and fall back to the canonical on-disk package name.
                pkg = __package__ or 'PyRePrism.languages'
                # First try a relative import using this module's package
                try:
                    importlib.import_module(f'.{name.lower()}', pkg)
                except Exception:
                    # Fall back to importing using the actual on-disk package
                    # directory name. This avoids issues where the package was
                    # installed or imported with different capitalization.
                    try:
                        import os
                        # languages package is two levels up from this file
                        package_dir = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
                        importlib.import_module(f'{package_dir}.languages.{name.lower()}')
                    except Exception:
                        # As a last resort, try a couple of common casing variants
                        for candidate in ('PyReprism', 'PyRePrism'):
                            try:
                                importlib.import_module(f'{candidate}.languages.{name.lower()}')
                                break
                            except Exception:
                                continue
            except Exception:
                # import failed or module doesn't exist; fall through
                pass
        return cls._registry.get(name)

    @classmethod
    def all(cls):
        return dict(cls._registry)
