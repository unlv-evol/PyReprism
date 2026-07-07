import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Pure(BaseLanguage):
    """Pure language support (``//`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.pure

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'ans|break|bt|case|const|def|else|end|extern|false|force|if|infix|infixl|infixr|'
            'interface|let|namespace|nonfix|of|otherwise|outfix|postfix|prefix|private|public|'
            'quote|then|true|type|using|when|with'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*.*?\*/|#!.*?$)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^/#"]*)',
            re.DOTALL | re.MULTILINE,
        )
