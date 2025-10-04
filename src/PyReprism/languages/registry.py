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
                importlib.import_module(f'.{name.lower()}', 'PyReprism.languages')
            except Exception:
                # import failed or module doesn't exist; fall through
                pass
        return cls._registry.get(name)

    @classmethod
    def all(cls):
        return dict(cls._registry)
