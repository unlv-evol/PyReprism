import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Rip(BaseLanguage):
    """Rip language support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.rip

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'case|catch|class|else|exit|finally|if|switch|try|throw|'
            'true|false|nil|return'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^#\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
