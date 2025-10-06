import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Asciidoc(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for Asciidoc files.

        :rtype: str
        """
        return extension.asciidoc

    @classmethod
    def keywords(cls) -> list:
        """Return a minimal keyword list for Asciidoc (currently empty).

        :rtype: list
        """
        return []

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex that captures Asciidoc comment forms.

        :rtype: re.Pattern
        """
        # Match // single-line and //// delimited blocks conservatively
        return re.compile(r'(?P<comment>//.*?$|////[\s\S]*?////)|(?P<noncomment>[^/\n][^\n]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return a placeholder regex for numeric literals.

        :rtype: re.Pattern
        """
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        """Return a placeholder regex for operators.

        :rtype: re.Pattern
        """
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        """Compile and return keywords regex.

        :rtype: re.Pattern
        """
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from Asciidoc source.

        :param source_code: the Asciidoc text
        :type source_code: str
        :param isList: if True return a list of fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove keywords from the input string.

        :param source: input string
        :type source: str
        :rtype: str
        """
        return re.sub(re.compile(cls.keywords_regex()), '', source)
