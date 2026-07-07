import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Soy(BaseLanguage):
    """Closure Templates (Soy) support (``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.soy

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'namespace|template|param|call|delcall|deltemplate|delpackage|'
            'if|elseif|else|switch|case|default|foreach|ifempty|for|let|literal|'
            'msg|fallbackmsg|print|css|xid|as|and|or|not|in|nil|true|false'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
