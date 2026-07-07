import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Haskell(BaseLanguage):
    """Haskell support (``--`` line and ``{- -}`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.haskell

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'case|class|data|deriving|do|else|if|in|infixl|infixr|instance|let|module|newtype|'
            'of|primitive|then|type|where'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>--.*?$|\{-[\s\S]*?-\}|\{-.*?$|^.*?-\})|'
            r'(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^-\{\'"]*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(r'\b(?:\d+(?:\.\d+)?(?:e[+-]?\d+)?|0o[0-7]+|0x[0-9a-f]+)\b')
