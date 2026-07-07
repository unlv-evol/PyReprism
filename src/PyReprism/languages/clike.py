import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Clike(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.clike

    @classmethod
    def keywords(cls) -> list:
        return 'if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue|true|false|class|interface|extends|implements|trait|instanceof|new'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|.[^/\'\"]*)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&?|\|\|?|\?|\*|\/|~|\^|%')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return ''.join(res)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
