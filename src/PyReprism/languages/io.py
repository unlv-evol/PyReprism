import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry

@LanguageRegistry.register
class IO(BaseLanguage):
    """IO language minimal support.
    Handles line-oriented comments (lines starting with #) vs non-comment lines.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.io

    @classmethod
    def keywords(cls) -> list:
        return ''.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#.*?$|//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>"[^"\n]*"|.[^#/"]*)', re.DOTALL | re.MULTILINE)

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