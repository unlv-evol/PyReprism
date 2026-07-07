import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Parser(BaseLanguage):
    """Parser (Parser 3) support (``#`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.parser

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'if|else|elsif|switch|case|default|while|break|continue|return|'
            'true|false|def|class|method|import'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^#/"]*)',
            re.DOTALL | re.MULTILINE,
        )
