import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class PHP(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.php

    @classmethod
    def keywords(cls) -> list:
        return 'and|or|xor|array|as|break|case|cfunction|class|const|continue|declare|default|die|do|else|elseif|enddeclare|endfor|endforeach|endif|endswitch|endwhile|extends|for|foreach|function|include|include_once|global|if|new|return|static|switch|use|require|require_once|var|while|abstract|interface|public|implements|private|protected|parent|throw|null|echo|print|trait|namespace|final|yield|goto|instanceof|finally|try|catch'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r"""(?P<comment>#.*?$|//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>'(\\.|[^\\'])*'|"(\\.|[^\\"])*"|.[^#/\'"{}]*)""", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[bo])?(?:(?:\d|0x[\da-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b', re.IGNORECASE)

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'[-+%=]=?|!=|\*\*?=?|//?=?|<[<=>]?|>[=>]?|[&|^~]|\b(?:or|and|not)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@<>$]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|null)\b', re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
