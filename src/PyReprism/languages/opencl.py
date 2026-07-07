import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class OpenCL(BaseLanguage):
    """OpenCL C language support (C-style ``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.opencl

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            '__kernel|kernel|__global|global|__local|local|__constant|constant|__private|private|'
            '__read_only|__write_only|__read_write|read_only|write_only|read_write|'
            'if|else|for|while|do|switch|case|default|break|continue|return|goto|'
            'void|char|uchar|short|ushort|int|uint|long|ulong|float|double|half|bool|size_t|'
            'const|volatile|restrict|static|inline|sizeof|struct|union|enum|typedef'
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
        return re.compile(r'\b0x[\da-fA-F]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?[fFuUlL]*')
