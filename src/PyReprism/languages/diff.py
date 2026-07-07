import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Diff(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.diff

    @classmethod
    def keywords(cls) -> list:
        keyword = ''.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        # line-oriented diff comments (lines starting with #) vs non-comment lines
        pattern = re.compile(r'(?P<comment>^#.*?$)|(?P<noncomment>^[^#\n].*?$)', re.MULTILINE)
        return pattern

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
