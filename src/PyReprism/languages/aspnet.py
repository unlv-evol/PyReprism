import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Aspnet(BaseLanguage):
    """ASP.NET / ASP flavor helper (handles HTML comments too)."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.aspnet

    @classmethod
    def keywords(cls) -> list:
        return 'Assembly|Control|Implements|Import|Master(?:Type)?|OutputCache|Page|PreviousPageType|Reference|Register'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Match C-style block comments, // line comments and HTML comments <!-- -->
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/|<!--[\s\S]*?-->)|(?P<noncomment>[^/<!]*[^\n]*)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls):
        # No number regex defined previously; return a regex that matches nothing
        return re.compile(r'^$')

    @classmethod
    def operator_regex(cls):
        # No operator regex defined previously; return a regex that matches nothing
        return re.compile(r'^$')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
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
        return re.sub(cls.keywords_regex(), '', source)
