import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class MakeFile(BaseLanguage):
    """Makefile support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.makefile

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'ifeq|ifneq|ifdef|ifndef|else|endif|include|define|endef|override|export|'
            'unexport|vpath'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#.*?$)|(?P<noncomment>.[^#]*)',
            re.DOTALL | re.MULTILINE,
        )
