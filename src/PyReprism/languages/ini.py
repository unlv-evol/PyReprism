
from .base import BaseLanguage
from .registry import LanguageRegistry
import re
from PyReprism.utils import extension



@LanguageRegistry.register
class INI(BaseLanguage):
    """INI / .ini / Windows INI style files."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.ini

    @classmethod
    def keywords(cls) -> list:
        # INI files generally don't have a language keyword set; keep empty.
        return []

    @classmethod
    def comment_regex(cls):
        # Match either a full-line comment starting with ';' or capture non-comment segments.
        # Provide named groups 'comment' and 'noncomment' as required by BaseLanguage.
        return re.compile(r'(?P<comment>^[ \t]*;.*$)|(?P<noncomment>[^;\n]*(?:\n|$))', re.MULTILINE)

    # number_regex and operator_regex default to BaseLanguage implementations

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return super().remove_keywords(source)



