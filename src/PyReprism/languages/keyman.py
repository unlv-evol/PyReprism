import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Keyman(BaseLanguage):
    """Keyman keyboard mapping language (.kmn).

    This is a minimal implementation: Keyman files use simple line comments in
    a few styles; we provide a forgiving comment regex and basic helpers so
    the rest of the toolchain can operate consistently.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.keyman

    @classmethod
    def keywords(cls) -> list:
        # Keyman files are mostly data; keep keywords list empty for now.
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """Return a regex with named groups 'comment' and 'noncomment'.

        Accept common single-line comment forms used in keyboard mapping files
        (leading 'c ' lines, semicolon, hash, and C-style //). There are no
        widely used block-comments in Keyman, so we keep the pattern simple.
        """
        return re.compile(
            r"(?P<comment>//.*?$|#.*?$|;.*?$|^c\s.*?$)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/;#'\"\n]+)",
            re.MULTILINE,
        )

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
