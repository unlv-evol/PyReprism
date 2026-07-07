import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class RenPy(BaseLanguage):
    """Ren'Py script support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.renpy

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'label|menu|scene|show|hide|with|play|stop|queue|pause|jump|call|return|'
            'define|default|image|transform|screen|python|init|if|elif|else|while|for|in|'
            'pass|at|as|expression|onlayer|zorder|behind|nvl|window|voice|text|True|False|None'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^#\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
