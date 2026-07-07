import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Oz(BaseLanguage):
    """Oz language support (``%`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.oz

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'declare|local|in|end|proc|fun|functor|class|meth|attr|feat|from|prop|'
            'if|then|else|elseif|elsecase|case|of|for|do|while|try|catch|finally|raise|'
            'thread|lock|or|dis|choice|not|cond|andthen|orelse|div|mod|true|false|unit|nil'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>%.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^%/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
