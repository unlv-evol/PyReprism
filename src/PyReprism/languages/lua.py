import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry

@LanguageRegistry.register
class LUA(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.lua

    @classmethod
    def keywords(cls) -> list:
        return 'and|break|do|else|elseif|end|false|for|function|if|in|local|nil|not|or|repeat|return|then|true|until|while'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>--\[\[.*?\]\]|--.*?$)|(?P<noncomment>[^-\n]+)', re.DOTALL | re.MULTILINE)

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

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)