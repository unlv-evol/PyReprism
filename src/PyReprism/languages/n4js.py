import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class N4js(BaseLanguage):
    """N4JS support (``//`` and ``/* */`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.n4js

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|'
            'extends|finally|for|function|if|import|in|instanceof|new|null|return|super|switch|'
            'this|throw|try|typeof|var|void|while|with|yield|let|await|async|'
            'implements|interface|package|private|protected|public|static|get|set|'
            'true|false|abstract'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|\'(\\.|[^\\\'])*\'|.[^/\'"]*)',
            re.DOTALL | re.MULTILINE,
        )
