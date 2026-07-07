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
        """Return a regex to match ERB comments and non-comment text.

        :rtype: re.Pattern
        """
        return re.compile(r'(?P<comment><!--.*?-->|#.*?$)|(?P<noncomment>[^#<\n]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from the given ERB source code.

        :param source_code: The ERB source code to process.
        :param isList: If True, return a list of non-comment segments; otherwise, return a single string.
        :rtype: str or list[str]    
        """
        result = []
        for match in cls.comment_regex().finditer(source_code):
            non = match.groupdict().get('noncomment')
            if non:
                result.append(non)
        if isList:
            return result
        return ''.join(result)
