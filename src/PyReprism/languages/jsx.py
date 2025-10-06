import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Jsx(BaseLanguage):
    """JSX/React-like language helper migrated to BaseLanguage.

    Keeps comment-removal semantics from the original implementation
    (only append non-empty 'noncomment' matches). Keywords removal is
    delegated to the base class.
    """

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for JSX/TSX files.

        :rtype: str
        """
        return extension.jsx

    @classmethod
    def keywords(cls) -> list:
        """Return a list of JavaScript/JSX keywords used for token filtering.

        :rtype: list
        """
        return 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """Compile and return a regex that captures comments and non-comment
        fragments in JSX-like source.

        The pattern includes single-line // comments, C-style /* ... */ block
        comments, and JSX fragments like {/* ... */}. It provides named groups
        ``comment`` and ``noncomment`` as required by BaseLanguage helpers.

        :rtype: re.Pattern
        """
        # Line comments, C-style block comments, and JSX-style {/* ... */} blocks
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/|\{/\*[\s\S]*?\*/\})|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"\n]+)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """Return a regex matching numeric literals used in JSX/JavaScript.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:0[xX][\dA-Fa-f]+|0[bB][01]+|0[oO][0-7]+|NaN|Infinity)\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        """Return a regex matching common JavaScript operators.

        :rtype: re.Pattern
        """
        return re.compile(r'-[-=]?|\+[+=]?|!=?=?|<<?=?|>>?>?=?|=(?:==?|>)?|&[&=]?|\|[|=]?|\*\*?=?|\/?=|~|\^=?|%=?|\?|\.\.\.')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Compile a regex that matches any of the language keywords.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        """Return a regex matching delimiter characters used in JSX/JS.

        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        """Return a regex matching boolean-like literals.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|null)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from source, returning either the joined string
        or a list of non-comment fragments when isList is True.

        :param source_code: the source text to process
        :type source_code: str
        :param isList: if True return list of fragments instead of string
        :type isList: bool
        :rtype: list[str] or str
        """
        result = []
        for match in cls.comment_regex().finditer(source_code):
            non = match.groupdict().get('noncomment')
            if non:
                result.append(non)
        if isList:
            return result
        return ''.join(result)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        """Remove known keywords from the source using BaseLanguage helper.

        :param source: input source text
        :type source: str
        :rtype: str
        """
        return super().remove_keywords(source)
