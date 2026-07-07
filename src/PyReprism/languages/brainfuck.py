import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class BrainFuck(BaseLanguage):
    """Brainf*ck language helper.

    Brainf*ck doesn't have textual keywords; it uses single-character operators.
    This class focuses on preserving the operators and stripping all other
    non-operator characters (treated as comments/non-code in many contexts).
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.brainfuck

    @classmethod
    def keywords(cls) -> list:
        # No keywords in Brainfuck; return empty list so keywords_regex matches nothing.
        return []

    @classmethod
    def comment_regex(cls):
        # Keep operator characters in 'noncomment' group and treat everything else as 'comment'.
        return re.compile(r'(?P<comment>[^><+\-.,\[\]]+)|(?P<noncomment>[><+\-.,\[\]])')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'[><+\-.,\[\]]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return super().remove_keywords(source)

