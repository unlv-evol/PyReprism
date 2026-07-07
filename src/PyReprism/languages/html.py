import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class HTML(BaseLanguage):
    """HTML support (``<!-- -->`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.html

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

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Strip HTML comments.

        :param source_code: The HTML source to process.
        :param isList: If True, return a list of non-comment segments.
        :rtype: str or list[str]
        """
        if isList:
            return super().remove_comments(source_code, isList=True)
        return super().remove_comments(source_code).strip()
