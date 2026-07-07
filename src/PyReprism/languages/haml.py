import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Haml(BaseLanguage):
    """Haml template support (``-#`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.haml

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>^-#.*?$|^-#[\s\S]*?(?=\n\S)|^-#[\s\S]*?$)|'
            r'(?P<noncomment>[^\n]*?(?=\n\S|$))',
            re.MULTILINE,
        )
