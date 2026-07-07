import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Velocity(BaseLanguage):
    """Apache Velocity support (``##`` line and ``#* *#`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.velocity

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            '#set|#if|#elseif|#else|#end|#foreach|#include|#parse|#macro|#break|#stop|'
            '#evaluate|#define'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>##.*?$|#\*[\s\S]*?\*#)|(?P<noncomment>.[^#]*)',
            re.DOTALL | re.MULTILINE,
        )
