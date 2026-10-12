import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Flow(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.flow

    @classmethod
    def keywords(cls) -> list:
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Strings and template literals are kept whole.
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>\"(?:\\.|[^\\\"\n])*\"|'(?:\\.|[^\\'\n])*'|`(?:\\.|[^\\`])*`|.[^/\"'`]*)",
            re.DOTALL | re.MULTILINE)

