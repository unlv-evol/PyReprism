import re
from PyRePrism.utils import extension
from PyRePrism.languages.base import BaseLanguage
from PyRePrism.languages.registry import LanguageRegistry


@LanguageRegistry.register
class CSP(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.csp

    @classmethod
    def keywords(cls) -> list:
        # Common CSP directives
        return [
            'default-src','script-src','style-src','img-src','connect-src','font-src','object-src','media-src','frame-src',
            'base-uri','form-action','frame-ancestors','report-uri','report-to','require-sri-for','sandbox','block-all-mixed-content','upgrade-insecure-requests'
        ]

    @classmethod
    def comment_regex(cls):
        # CSP is typically header text — use a conservative non-comment match
        return re.compile(r'(?P<noncomment>.+)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(re.escape(k) for k in cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
