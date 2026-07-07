import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Yaml(BaseLanguage):
    """YAML support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.yaml

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return ['true', 'false', 'null', 'yes', 'no', 'on', 'off']

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$)|(?P<noncomment>.[^#]*)',
            re.DOTALL | re.MULTILINE,
        )
