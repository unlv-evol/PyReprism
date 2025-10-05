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
        # Scheme: ; line comments, and block comments #| ... |#
        return re.compile(r"(?P<comment>;.*?$|#\|[\s\S]*?\|#)|(?P<noncomment>[^;#\n]+)", re.DOTALL | re.MULTILINE)

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
    def remove_comments(cls, source_code: str, isList: bool = False):
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
        return super().remove_keywords(source)
