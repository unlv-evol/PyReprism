import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Batch(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.batch

    @classmethod
    def keywords(cls) -> list:
        keyword = 'not|cmdextversion|defined|errorlevel|exist|echo|set'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>\bREM\b.*?$|::.*?$)|(?P<noncomment>.[^:R]*)', re.DOTALL | re.MULTILINE | re.IGNORECASE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'\^|==|\b(?:equ|neq|lss|leq|gtr|geq)\b|([*\/%%+\-&^|]=?|<<=?|>>=?|[!~_=])', re.IGNORECASE)

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
