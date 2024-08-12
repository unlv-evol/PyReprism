import re
from PyReprism.utils import extension


class Vbnet:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.vbnet

    @staticmethod
    def keywords() -> list:
        keyword = ''.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>\'.*?$)|(?P<noncomment>[^\'\n]*[^\n]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        pattern = re.compile(r'')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(Vbnet.keywords()) + r')\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify VB.NET language delimiters.

        This function generates a regular expression that matches VB.NET language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, and angle brackets `<`, `>`, as well as the ampersand `&`.

        :return: A compiled regex pattern to match VB.NET delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;<>&]')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify VB.NET boolean literals.

        This function generates a regular expression that matches the VB.NET boolean literals `True`, `False`, and the special constant `Nothing`.

        :return: A compiled regex pattern to match VB.NET boolean literals and `Nothing`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:True|False|Nothing)\b', re.IGNORECASE)

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        return Vbnet.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Vbnet.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Vbnet.keywords_regex()), '', source)
