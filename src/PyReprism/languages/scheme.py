import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Scheme(BaseLanguage):
    """Scheme/Racket-like language helpers."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.scheme

    @classmethod
    def keywords(cls) -> list:
        # No keywords defined previously
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Strings and character literals such as #\; are kept whole.
        return re.compile(
            r"(?P<comment>;.*?$|#\|[\s\S]*?\|#)|(?P<noncomment>#\\.|\"(?:\\.|[^\\\"])*\"|.[^;#\"]*)",
            re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        # No number regex previously; return a noop pattern
        return re.compile(r'^$')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'^$')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r"^$")

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
