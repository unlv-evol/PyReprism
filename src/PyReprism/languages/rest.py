import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Rest(BaseLanguage):
    """reStructuredText support (``..`` explicit-markup comment lines)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.rest

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """A reST comment is a ``..`` block not followed by a directive/target.

        :rtype: re.Pattern
        """
        return re.compile(
            r'(?P<comment>^\.\.[ \t]+(?![\w.-]+::|_|\[|\|)[^\n]*$)|'
            r'(?P<noncomment>.[^\n]*|\n)',
            re.MULTILINE,
        )
