import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class SmallTalk(BaseLanguage):
    """Smalltalk language helper."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.smalltalk

    @classmethod
    def keywords(cls) -> list:
        # Smalltalk has no keyword list here
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r'(?P<comment>".*?"|".*?$|^.*?")|(?P<noncomment>[^\"]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        # No number pattern defined; return a no-match pattern
        return re.compile(r'(?!x)x')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(?!x)x')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        kws = cls.keywords()
        if not kws:
            return re.compile(r'(?!x)x')
        return re.compile(r'\b(' + '|'.join(kws) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve previous behavior: collect noncomment matches when truthy
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
