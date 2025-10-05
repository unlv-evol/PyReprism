import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Julia(BaseLanguage):
    """Julia language helper.

    Handles Julia comments (`#` and block comments `#= ... =#`), numbers,
    operators and a conservative keyword list.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.julia

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|baremodule|begin|bitstype|break|catch|ccall|const|continue|do|else|elseif|end|export|finally|for|function|global|if|immutable|import|importall|let|local|macro|module|print|println|quote|return|try|type|typealias|using|while|true|false'.split('|')

    @classmethod
    def comment_regex(cls):
        # Support single-line '#' and block comments '#= ... =#'
        return re.compile(r'(?P<comment>#=.*?$|#=[\s\S]*?=#|#.*?$)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|[^#\'\"]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[box])?(?:[\da-f]+\.?\d*|\.\d+)(?:[efp][+-]?\d+)?j?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'[-+*^%÷&$\\]=?|\/[\/=]?|!=?=?|\|[=>]?|<(?:<=?|[=:])?|>(?:=|>>?=?)?|==?=?|[~≠≤≥]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return super().remove_keywords(source)
