import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class JavaScript(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.javascript

    @classmethod
    def keywords(cls) -> list:
        return 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Match C-style // line comments and /* block comments; preserve
        # string literals and other non-comment sequences as 'noncomment'.
        # Do not treat braces as comments.
        # Allow newlines in noncomment groups so original line breaks are
        # preserved when comments are removed.
        return re.compile(r"(?P<comment>//.*?$|/\*.*?\*/)|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|[^/\\'\"]+)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:0[xX][\dA-Fa-f]+|0[bB][01]+|0[oO][0-7]+|NaN|Infinity)\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'-[-=]?|\+[+=]?|!=?=?|<<?=?|>>?>?=?|=(?:==?|>)?|&[&=]?|\|[|=]?|\*\*?=?|\/?=?|~|\^=?|%=?|\?|\.{3}')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
