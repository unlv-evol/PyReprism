import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Puppet(BaseLanguage):
    """Puppet manifest support (``#`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.puppet

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'class|define|node|inherits|if|elsif|else|case|default|and|or|in|import|'
            'include|require|contain|create_resources|unless|type|attr|function|'
            'true|false|undef'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^#/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
