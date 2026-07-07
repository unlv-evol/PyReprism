import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Go(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.go

    @classmethod
    def keywords(cls) -> list:
        return 'break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go(?:to)?|if|import|interface|map|package|range|return|select|struct|switch|type|var|bool|byte|complex(?:64|128)|error|float32|float64|rune|string|u?int(?:8|16|32|64)?|uintptr|append|cap|close|complex|copy|delete|imag|len|make|new|panic|print|println|real|recover|iota|nil|true|false'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|.[^/\\'\"]*)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'[*\/%^!=]=?|\+[=+]?|-[=-]?|\|[=|]?|&(?:=|&|\^=?)?|>(?:>=?|=)?|<(?:<=?|=|-)?|:=|\.\.\.')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;]|\.{3}')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|nil)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
