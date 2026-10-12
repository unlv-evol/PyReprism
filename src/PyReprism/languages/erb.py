import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Erb(BaseLanguage):
    """Minimal stub for ERB (Embedded Ruby) language. Provides comment removal and basic token regexes.
    """
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension for ERB files.

        :rtype: str
        """
        return extension.erb

    @classmethod
    def keywords(cls) -> list:
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Comments are <%# %> tags and HTML comments; # in markup is text.
        return re.compile(
            r"(?P<comment><%#[\s\S]*?%>|<!--[\s\S]*?-->)|(?P<noncomment>.[^<]*)",
            re.DOTALL | re.MULTILINE)

