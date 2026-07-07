import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry

@LanguageRegistry.register
class MEL(BaseLanguage):
    """MEL (Maya Embedded Language) minimal support.
    Handles C-style single-line comments (//) vs non-comment lines."""
    @classmethod
    def file_extension(cls) -> str:
        return extension.mel

    @classmethod
    def keywords(cls) -> list:
        return 'break|case|catch|continue|default|do|else|elseif|end|for|global|if|in|local|proc|return|switch|then|while'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>//.*?$)|(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^/\'"]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/?=|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return ''.join(res)