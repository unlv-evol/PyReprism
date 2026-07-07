import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Processing(BaseLanguage):
    """Processing language support (Java-like ``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.processing

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'if|else|for|while|do|switch|case|default|break|continue|return|new|'
            'class|extends|implements|interface|public|private|protected|static|final|'
            'abstract|void|boolean|byte|char|short|int|long|float|double|color|'
            'String|true|false|null|this|super|import|try|catch|finally|throw|throws|'
            'setup|draw|size|background|fill|stroke|noFill|noStroke'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(r'\b0x[\da-fA-F]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?[fFdDlL]?')
