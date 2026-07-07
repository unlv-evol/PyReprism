import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Reason(BaseLanguage):
    """ReasonML support (``/* */`` block and ``//`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.reason

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'and|as|assert|begin|class|constraint|else|end|exception|external|for|fun|function|'
            'functor|if|in|include|inherit|initializer|lazy|let|method|module|mutable|new|'
            'nonrec|object|of|open|or|pri|pub|rec|switch|then|to|try|type|val|virtual|when|'
            'while|with|true|false'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^/"]*)',
            re.DOTALL | re.MULTILINE,
        )
