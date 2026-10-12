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
        # Quoted values (e.g. URLs) are kept whole.
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/|<!--[\s\S]*?-->|<%--[\s\S]*?--%>)|(?P<noncomment>\"(?:\\.|[^\\\"\n])*\"|'(?:\\.|[^\\'\n])*'|.[^/<\"']*)",
            re.DOTALL | re.MULTILINE)

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
    def remove_keywords(cls, source: str) -> str:
        """Remove keywords from the input source text.

        :param source: input source
        :type source: str
        :rtype: str
        """
        return re.sub(cls.keywords_regex(), '', source)
