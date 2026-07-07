import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class MarkDown(BaseLanguage):
    """Markdown support (embedded HTML ``<!-- -->`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.markdown

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment><!--[\s\S]*?-->)|(?P<noncomment>.[^<]*)',
            re.DOTALL | re.MULTILINE,
        )
