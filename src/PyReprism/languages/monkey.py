import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Monkey(BaseLanguage):
    """Monkey X support (``'`` line and ``#Rem ... #End`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.monkey

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'Function|Method|Class|Interface|Extends|Implements|Import|Module|Strict|Public|'
            'Private|Property|Field|Global|Local|Const|Return|New|Self|Super|Extern|'
            'If|Then|Else|ElseIf|EndIf|While|Wend|Repeat|Until|Forever|For|To|Step|Next|'
            'Select|Case|Default|End|Throw|Try|Catch|Print|And|Or|Not|Mod|Shl|Shr|'
            'True|False|Null|Void|Int|Float|String|Bool|Array|Object|Continue|Exit|Eachin'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>#[Rr]em[\s\S]*?#[Ee]nd|\'.*?$)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^\'#"]*|[#\'])',
            re.DOTALL | re.MULTILINE,
        )
