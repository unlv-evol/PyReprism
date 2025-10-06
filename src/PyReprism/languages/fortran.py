import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class ForTran(BaseLanguage):
    """Fortran language helper (minimal)."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.fortran

    @classmethod
    def keywords(cls) -> list:
        # Keep the original token list but guard against mis-formed entries
        return [
            'INTEGER', 'REAL', 'DOUBLE', 'PRECISION', 'COMPLEX', 'CHARACTER', 'LOGICAL'
        ]

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r'(?P<comment>!.*?$)|(?P<noncomment>[^!\n]+)', re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[ED][+-]?\d+)?(?:_\w+)?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'\*\*|\/\/|=>|[=\/]=|[<>]=?|::|[+\-*=%]|\.(?:EQ|NE|LT|LE|GT|GE|NOT|AND|OR|EQV|NEQV)\.|\.[A-Z]+\.')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

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
