import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Mizar(BaseLanguage):
    """Mizar support (``::`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.mizar

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'environ|begin|theorem|scheme|proof|end|for|ex|being|such|that|holds|st|'
            'let|assume|thus|hence|then|by|from|def|definition|redefine|means|equals|'
            'reserve|consider|take|per|cases|suppose|now|and|or|not|implies|iff'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>::.*?$)|(?P<noncomment>.[^:]*|:)',
            re.DOTALL | re.MULTILINE,
        )
