import re
from PyReprism.utils import extension


class Bash:
    """
    This is the class for processing Bash source code
    """
    def __init__() -> None:
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.bash

    @staticmethod
    def keywords() -> list:
        keyword = 'if|then|else|elif|fi|for|break|continue|while|in|case|function|select|do|done|until|echo|exit|return|set|declare|let'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Bash operators.

        :return: A compiled regex pattern to match various Python operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/=?|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:')
        return pattern

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Bash boolean literals.

        :return: A compiled regex pattern to match Bash boolean literals and `None`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(^|[\s;|&])(?:true|false)(?=$|[\s;|&])\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Bash delimiters.

        :return: A compiled regex pattern to match Bash delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'\$?\(\(?|\)\)?|\.\.|[{}[\];]')

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Bash keywords.

        :return: A compiled regex pattern to match Bash keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(Bash.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Bash source code string.

        :param str source_code: The Bash source code from which to remove comments.
        :param bool isList: (Optional) A flag indicating if the input is a list of source code lines. This parameter is not used in the function logic.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Bash.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Bash.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        """
        Remove all Bash keywords from the provided source code string.

        :param str source: The source code string from which to remove Python keywords.
        :return: The source code string with all Bash keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Bash.keywords_regex()), '', source)
