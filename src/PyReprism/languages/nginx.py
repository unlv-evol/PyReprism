import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Nginx(BaseLanguage):
    """Nginx configuration language helper.

    Keeps comment handling for `#` comments and preserves text outside
    comments in the 'noncomment' group required by BaseLanguage.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.nginx

    @classmethod
    def keywords(cls) -> list:
        # Nginx uses directives rather than traditional keywords; keep empty
        # for now and expand later if you want directive-aware removal.
        return []

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]*(?:\n|$))', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b\d+\b')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'[{};=]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return super().remove_keywords(source)
