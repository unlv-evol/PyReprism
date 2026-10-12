import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Properties(BaseLanguage):
    """.properties files support (``#`` and ``!`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.properties

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Only lines that start with # or ! are comments.
        return re.compile(
            r"(?P<comment>^[ \t]*[#!].*?$)|(?P<noncomment>[^\n]+|\n)",
            re.DOTALL | re.MULTILINE)
