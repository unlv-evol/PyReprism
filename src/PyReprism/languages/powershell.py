import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class PowerShell(BaseLanguage):
    """PowerShell support (``#`` line and ``<# #>`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.powershell

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'begin|break|catch|class|continue|data|define|do|dynamicparam|else|elseif|end|'
            'exit|filter|finally|for|foreach|from|function|if|in|param|process|return|switch|'
            'throw|trap|try|until|using|var|while|workflow'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment><#.*?#>|#.*?$)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^#<\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
