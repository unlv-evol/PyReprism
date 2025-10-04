import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Bash(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.bash

    @classmethod
    def keywords(cls) -> list:
        return ''.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>'"'(\\.|[^\\'])*'"'|"(\\.|[^\\"])*"|.[^#\'\"]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/?=|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return ''.join(res)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
