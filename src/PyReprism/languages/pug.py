import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Pug(BaseLanguage):
    """Pug (Jade) template support (``//`` and ``//-`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.pug

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'if|else|unless|case|when|default|each|while|for|in|block|extends|include|'
            'append|prepend|mixin|append|doctype|yield'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Comments take their own line; // in text or attributes is code.
        return re.compile(
            r"(?P<comment>^[ \t]*//-?.*?$)|(?P<noncomment>[^\n]+|\n)",
            re.DOTALL | re.MULTILINE)
