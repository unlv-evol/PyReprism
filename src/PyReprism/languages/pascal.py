import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Pascal(BaseLanguage):
    """Pascal support (``(* *)``, ``{ }`` and ``//`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.pascal

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'absolute|array|asm|begin|case|const|constructor|destructor|do|downto|else|end|file|'
            'for|function|goto|if|implementation|inherited|inline|interface|label|nil|object|of|'
            'operator|packed|procedure|program|record|reintroduce|repeat|self|set|string|then|to|'
            'type|unit|until|uses|var|while|with|dispose|exit|false|new|true|class|except|exports|'
            'finalization|finally|initialization|library|on|out|property|raise|threadvar|try|'
            'abstract|private|protected|public|published|virtual|override|overload'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|\(\*[\s\S]*?\*\)|\{[\s\S]*?\})|'
            r'(?P<noncomment>\'(\\.|\'\'|[^\'])*\'|.[^/({\']*|[/({])',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(r'\$[0-9a-f]+|\b\d+(?:\.\d+)?(?:e[+-]?\d+)?', re.IGNORECASE)

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Case-insensitive keyword matcher (Pascal is case-insensitive).

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)
