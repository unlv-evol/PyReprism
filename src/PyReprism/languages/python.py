import re
from PyReprism.utils import extension


class Python:
    """
    This is the class for processing Python source code
    """
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for Python files.

        :return: The file extension for Python files.
        :rtype: str
        """
        return extension.python

    @staticmethod
    def keywords() -> list:
        """
        Return a list of Python keywords and built-in functions.

        :return: A list of Python keywords and built-in function names.
        :rtype: list
        """
        keyword = 'as|assert|async|await|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|nonlocal|pass|print|raise|return|try|while|with|yield|__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|case|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|match|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip|True|False|None'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in Python source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>#.*?$)|'r'(?P<multilinecomment1>""".*?""")|'r'(?P<multilinecomment2>\'\'\'.*?\'\'\')|'r'(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in Python code.

        :return: A compiled regex pattern to match Python numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[bo])?(?:(?:\d|0x[\da-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b', re.IGNORECASE)
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python operators.

        :return: A compiled regex pattern to match various Python operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]|\b(?:or|and|not)\b')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python keywords.

        :return: A compiled regex pattern to match Python keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(Python.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python boolean literals.

        :return: A compiled regex pattern to match Python boolean literals and `None`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:True|False|None)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python delimiters.

        :return: A compiled regex pattern to match Python delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@]')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Python source code string.

        :param str source_code: The Python source code from which to remove comments.
        :param bool isList: (Optional) A flag indicating if the input is a list of source code lines. This parameter is not used in the function logic.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Python.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Python.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all Python keywords from the provided source code string.

        :param str source: The source code string from which to remove Python keywords.
        :return: The source code string with all Python keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Python.keywords_regex()), '', source)
