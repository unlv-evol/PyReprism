import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Smarty(BaseLanguage):
    """Smarty template support (``{* ... *}`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.smarty

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'if|elseif|else|foreach|foreachelse|for|while|section|sectionelse|'
            'literal|capture|include|assign|block|function|nocache|ldelim|rdelim|'
            'true|false|null|and|or|not|eq|neq|gt|lt|gte|lte'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>\{\*.*?\*\})|(?P<noncomment>.[^{]*|\{)',
            re.DOTALL | re.MULTILINE,
        )
