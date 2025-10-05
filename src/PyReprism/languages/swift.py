import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Swift(BaseLanguage):
    """Swift language helper."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.swift

    @classmethod
    def keywords(cls) -> list:
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>[^/\n]*[^\n]*)', re.DOTALL | re.MULTILINE)

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
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|nil)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;<>?!]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve legacy scalar behavior (substitution + strip)
        out = cls.comment_regex().sub(lambda match: match.groupdict().get('noncomment') or '', source_code).strip()
        if isList:
            return [out]
        return out

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
