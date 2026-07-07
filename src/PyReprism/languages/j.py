import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class J(BaseLanguage):
    """J language support (``NB.`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.j

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>NB\..*?$)|(?P<noncomment>.[^N]*)',
            re.DOTALL | re.MULTILINE,
        )
