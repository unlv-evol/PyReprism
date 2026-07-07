import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Scss(BaseLanguage):
    """SCSS support (``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.scss

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            '@import|@mixin|@include|@extend|@function|@return|@if|@else|@each|@for|@while|'
            '@media|@content|@use|@forward|@at-root|@debug|@warn|@error|!default|!important'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>.[^/]*)',
            re.DOTALL | re.MULTILINE,
        )
