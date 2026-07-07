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
        """Return the file extension used for Julia source files.

        :rtype: str
        """
        return extension.julia

    @classmethod
    def keywords(cls) -> list:
        """Return a conservative list of Julia keywords.

        :rtype: list
        """
        return 'abstract|baremodule|begin|bitstype|break|catch|ccall|const|continue|do|else|elseif|end|export|finally|for|function|global|if|immutable|import|importall|let|local|macro|module|print|println|quote|return|try|type|typealias|using|while|true|false'.split('|')

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex that captures Julia comments and non-comment code.

        Supports single-line comments starting with ``#`` and block comments
        delimited with ``#= ... =#``. The pattern provides named groups
        ``comment`` and ``noncomment`` so BaseLanguage helpers can extract
        non-comment fragments.

        :rtype: re.Pattern
        """
        # Support single-line '#' and block comments '#= ... =#'
        pattern = r'''(?P<comment>#=.*?$|#=[\s\S]*?=#|#.*?$)|(?P<noncomment>'(\\.|[^\\'])*'|"(\\.|[^\\"])*"|[^#'\"]+)'''
        return re.compile(pattern, re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return a regex that matches Julia numeric literals (heuristic).

        :rtype: re.Pattern
        """
        return re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[box])?(?:[\da-f]+\.?\d*|\.\d+)(?:[efp][+-]?\d+)?j?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'[-+*^%÷&$\\]=?|\/[\/=]?|!=?=?|\|[=>]?|<(?:<=?|[=:])?|>(?:=|>>?=?)?|==?=?|[~≠≤≥]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from Julia source using BaseLanguage helper.

        :param source_code: Julia source text
        :type source_code: str
        :param isList: if True return list of non-comment fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove known Julia keywords from the provided source.

        :param source: input source text
        :type source: str
        :rtype: str
        """
        return super().remove_keywords(source)
