import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Arff(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for ARFF files.

        :rtype: str
        """
        return extension.arff

    @classmethod
    def keywords(cls) -> list:
        """Return ARFF control keywords.

        :rtype: list
        """
        keyword = 'attribute|data|end|relation'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex that splits ARFF comments and data.

        :rtype: re.Pattern
        """
        return re.compile(r'(?P<comment>%.*?$)|(?P<noncomment>[^%]*)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return regex matching numeric literals (ints and floats).

        :rtype: re.Pattern
        """
        return re.compile(r'\b\d+(?:\.\d+)?\b')

    @classmethod
    def operator_regex(cls):
        """Return a placeholder operator regex.

        :rtype: re.Pattern
        """
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        """Compile and return the keywords regex for ARFF.

        :rtype: re.Pattern
        """
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comment lines starting with '%' from ARFF content.

        :param source_code: input ARFF text
        :type source_code: str
        :param isList: if True return list of non-comment fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        result = []
        for match in cls.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove ARFF keywords from the provided source string.

        :param source: input string
        :type source: str
        :rtype: str
        """
        return re.sub(re.compile(cls.keywords_regex()), '', source)
