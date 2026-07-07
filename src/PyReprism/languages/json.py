import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Json(BaseLanguage):
    """JSON support (JSONC-style ``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.json

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return ['true', 'false', 'null']

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^/"]*)',
            re.DOTALL | re.MULTILINE,
        )
