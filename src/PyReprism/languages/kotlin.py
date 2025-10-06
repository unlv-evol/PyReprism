import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Kotlin(BaseLanguage):
    """Kotlin language helper.

    Implements comment, number, operator, delimiter and keyword helpers for
    Kotlin. Delegates removal logic to BaseLanguage.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.kotlin

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|annotation|as|break|by|catch|class|companion|const|constructor|continue|crossinline|data|do|else|enum|final|finally|for|fun|get|if|import|in|init|inline|inner|interface|internal|is|lateinit|noinline|null|object|open|out|override|package|private|protected|public|reified|return|sealed|set|super|tailrec|this|throw|to|try|val|var|when|where|while'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"{}]+)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:0[bx][\da-fA-F]+|\d+(?:\.\d+)?(?:e[+-]?\d+)?[fFL]?)\b')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        # Conservative operator regex: symbols and common word-operators
        return re.compile(r'\+[+=]?|-[-=]?|==?=?|!=?=?|[/\*%<>]=?|\.|&&|\|\||\b(?:and|or|xor|shl|shr|ushr)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;<>?]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|null)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
