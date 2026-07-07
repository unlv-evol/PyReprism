import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Aspnet(BaseLanguage):
    """ASP.NET / ASP flavor helper (handles HTML comments too)."""

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for ASP.NET files.

        :rtype: str
        """
        return extension.aspnet

    @classmethod
    def keywords(cls) -> list:
        """Return a small set of ASP.NET-specific directive keywords.

        :rtype: list
        """
        return 'Assembly|Control|Implements|Import|Master(?:Type)?|OutputCache|Page|PreviousPageType|Reference|Register'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """Compile and return a regex that matches C-style, '//' and HTML comments.

        :rtype: re.Pattern
        """
        # Match C-style block comments, // line comments and HTML comments <!-- -->
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/|<!--[\s\S]*?-->|<%--[\s\S]*?--%>)|(?P<noncomment>.[^/<]*)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls):
        """Return a regex matching no numbers (placeholder).

        :rtype: re.Pattern
        """
        # No number regex defined previously; return a regex that matches nothing
        return re.compile(r'^$')

    @classmethod
    def operator_regex(cls):
        """Return a placeholder operator regex (matches nothing).

        :rtype: re.Pattern
        """
        # No operator regex defined previously; return a regex that matches nothing
        return re.compile(r'^$')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Compile and return the keywords regex for ASP.NET.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from ASP.NET/HTML-like content.

        Preserves non-comment fragments (including strings) and returns either
        a list of fragments or a joined string depending on ``isList``.

        :param source_code: input source text
        :type source_code: str
        :param isList: if True return a list of fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        # Preserve original behavior: only append truthy 'noncomment' groups.
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
        """Remove keywords from the input source text.

        :param source: input source
        :type source: str
        :rtype: str
        """
        return re.sub(cls.keywords_regex(), '', source)
