import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Less(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.less

    @classmethod
    def keywords(cls) -> list:
        return ''.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/*]*[^\n]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        keys = cls.keywords()
        if not keys:
            return re.compile(r'$^')
        return re.compile(r'\b(' + '|'.join(re.escape(k) for k in keys) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        kr = cls.keywords_regex()
        if kr.pattern == '$^':
            return source
        return re.sub(kr, '', source)
