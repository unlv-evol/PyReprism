"""The default, zero-dependency backend: the language's own regexes."""
from typing import List

from ..tokens import Token
from .base import Engine


class RegexEngine(Engine):
    """Tokenize using the language class's regex-based :meth:`tokenize`."""

    name = 'regex'

    def tokenize(self, source: str, language_cls) -> List[Token]:
        return language_cls.tokenize(source)
