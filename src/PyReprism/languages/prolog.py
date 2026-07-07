import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Prolog(BaseLanguage):
    """Prolog support (``%`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.prolog

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'is|mod|rem|xor|div|true|false|fail|halt|assert|asserta|assertz|retract|'
            'findall|bagof|setof|forall'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>%.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>.[^%/]*)',
            re.MULTILINE | re.DOTALL,
        )
