import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Sass(BaseLanguage):
    """Indented Sass support (``//`` silent and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.sass

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            '@import|@mixin|@include|@extend|@function|@return|@if|@else|@each|@for|@while|'
            '@media|@content|@use|@forward|@at-root|@debug|@warn|@error|!default|!important|'
            'from|through|to|in|and|or|not'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
