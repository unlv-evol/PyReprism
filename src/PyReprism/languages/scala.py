import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Scala(BaseLanguage):
    """Scala language helper.

    Provides keyword list and regex helpers for comment, number, operator, and
    delimiter handling. Delegates removal logic to BaseLanguage.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.scala

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|case|catch|class|def|do|else|extends|final|finally|for|forSome|if|implicit|import|lazy|match|new|null|object|override|package|private|protected|return|sealed|self|super|this|throw|trait|try|type|val|var|while|with|yield|String|Int|Long|Short|Byte|Boolean|Double|Float|Char|Any|AnyRef|AnyVal|Unit|Nothing'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|[^/\'"{}]+|/[^/*][^/\'"{}]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0x[\da-f]*\.?[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e\d+)?[dfl]?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/?=|%=?|\^=?|[?:~])')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|null)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;<>?_]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
