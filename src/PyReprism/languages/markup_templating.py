import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class MarkupTemplating(BaseLanguage):
    """Generic markup templating support (HTML ``<!-- -->`` comments).

    This is a base helper for template languages embedded in markup; it strips
    standard XML/HTML comments.
    """

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.markup_templating

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment><!--.*?-->)|(?P<noncomment>.[^<]*|<)',
            re.DOTALL | re.MULTILINE,
        )
