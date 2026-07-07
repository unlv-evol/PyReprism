import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class VisualBasic(BaseLanguage):
    """Visual Basic support (``'`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.visual_basic

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'Dim|Const|As|If|Then|Else|ElseIf|End|Select|Case|For|Each|Next|To|Step|While|Wend|'
            'Do|Loop|Until|Function|Sub|Return|Exit|Call|Class|Module|Property|Get|Set|New|'
            'Nothing|ByVal|ByRef|Optional|Public|Private|Protected|Friend|Shared|Static|'
            'And|Or|Not|Xor|Mod|Is|True|False'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>\'.*?$)|(?P<noncomment>.[^\']*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Case-insensitive keyword matcher (VB is case-insensitive).

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)
