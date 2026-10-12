import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry

@LanguageRegistry.register
class GraphSql(BaseLanguage):
    """GraphQL helper (minimal)."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.graphql

    @classmethod
    def keywords(cls) -> list:
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Block strings and strings are kept whole.
        return re.compile(
            r"(?P<comment>#.*?$)|(?P<noncomment>\"\"\"[\s\S]*?\"\"\"|\"(?:\\.|[^\\\"\n])*\"|.[^#\"]*)",
            re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'(?!x)x')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(?!x)x')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        kws = cls.keywords()
        if not kws:
            return re.compile(r'(?!x)x')
        return re.compile(r'\b(' + '|'.join(kws) + r')\b')

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
