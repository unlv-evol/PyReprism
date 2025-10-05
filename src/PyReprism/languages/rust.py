import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Rust(BaseLanguage):
    """Rust language helper.

    Provides comment/number/operator regexes and a list of Rust keywords.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.rust

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|alignof|as|be|box|break|const|continue|crate|do|else|enum|extern|false|final|fn|for|if|impl|in|let|loop|match|mod|move|mut|offsetof|once|override|priv|pub|pure|ref|return|sizeof|static|self|struct|super|true|trait|type|typeof|unsafe|unsized|use|virtual|where|while|yield'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Capture block and line comments as 'comment'. Preserve strings and
        # other non-comment content in 'noncomment'. This is conservative but
        # practical for removing comments while keeping code and string literals.
        return re.compile(
            r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>\'"""(\\.|[^\\\'])*\'"""|\"(\\.|[^\\\"])*\"|[^/\'\"]+|/[^/*][^/\'\"]*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:0x[\dA-Fa-f](?:_?[\dA-Fa-f])*|0o[0-7](?:_?[0-7])*|0b[01](?:_?[01])*|(\d(?:_?\d)*)?\.?\d(?:_?\d)*(?:[Ee][+-]?\d+)?)(?:_?(?:[iu](?:8|16|32|64)?|f32|f64))?\b')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'[-+*\/%!^]=?|=[=>]?|@|&[&=]?|\|[|=]?|<<?=?|>>?=?')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|None)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;<>?]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
