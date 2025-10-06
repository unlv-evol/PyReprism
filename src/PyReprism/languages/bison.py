import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Bison(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.bison

    @classmethod
    def keywords(cls) -> list:
        # Bison/Yacc directives typically start with % (e.g. %token, %start)
        return ['%token', '%left', '%right', '%nonassoc', '%start', '%union', '%type']

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>[^/\n][^\n]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'(^|[^@])\b(?:0x[\da-f]+|\d+)')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        kws = cls.keywords() or []
        if not kws:
            return re.compile(r'\b\B')
        return re.compile(r"\b(" + "|".join(re.escape(k) for k in kws) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
