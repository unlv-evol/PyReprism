import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class SAS(BaseLanguage):
    """SAS support (``/* */`` block comments).

    Note: SAS also has ``*...;`` statement comments, but those are ambiguous with
    the multiplication operator and are intentionally not stripped here.
    """

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.sas

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'data|run|proc|quit|set|merge|by|where|if|then|else|do|end|output|keep|drop|'
            'rename|retain|array|format|informat|label|length|input|infile|put|file|'
            'libname|filename|options|title|footnote|and|or|not|in|eq|ne|gt|lt|ge|le'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>/\*.*?\*/)|'
            r'(?P<noncomment>\'(\\.|\'\'|[^\'])*\'|"(\\.|""|[^"])*"|.[^/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Case-insensitive keyword matcher.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)
