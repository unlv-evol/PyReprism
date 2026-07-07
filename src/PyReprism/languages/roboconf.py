import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Roboconf(BaseLanguage):
    """Roboconf graph/instances support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.roboconf

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'import|facet|instance of|installer|children|exports|imports|name|count|'
            'extends|external'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$)|(?P<noncomment>.[^#]*)',
            re.DOTALL | re.MULTILINE,
        )
