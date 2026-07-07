import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Protobuf(BaseLanguage):
    """Protocol Buffers (.proto) support (C-style ``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.protobuf

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'syntax|package|import|public|option|message|enum|service|rpc|returns|'
            'oneof|map|reserved|extend|extensions|group|to|max|weak|'
            'required|optional|repeated|default|'
            'double|float|int32|int64|uint32|uint64|sint32|sint64|fixed32|fixed64|'
            'sfixed32|sfixed64|bool|string|bytes|true|false'
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
        return re.compile(r'\b0x[\da-fA-F]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')
