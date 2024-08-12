import re
from PyReprism.utils import extension


class Java:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for Java files.

        :return: The file extension for Java files.
        :rtype: str
        """
        return extension.java

    @staticmethod
    def keywords() -> list:
        """
        Return a list of Java keywords and built-in functions.

        :return: A list of Java keywords and built-in function names.
        :rtype: list
        """
        keyword = 'abstract|continue|for|new|switch|assert|default|goto|package|synchronized|boolean|do|if|private|this|break|double|implements|protected|throw|byte|else|import|public|throws|case|enum|instanceof|return|transient|catch|extends|int|short|try|char|final|interface|static|void|class|finally|long|strictfp|volatile|const|float|native|super|while'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in Java source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in Java code.

        :return: A compiled regex pattern to match Java numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Java operators.

        :return: A compiled regex pattern to match various Java operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/=?|%=?|\^=?|[?:~])')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Java keywords.

        :return: A compiled regex pattern to match Java keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(Java.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Java boolean literals.

        :return: A compiled regex pattern to match Java boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Java delimiters.

        :return: A compiled regex pattern to match Java delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @staticmethod
    def remove_comments(source_code: str) -> str:
        """
        Remove comments from the provided Java source code string.

        :param str source_code: The Java source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Java.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all Java keywords from the provided source code string.

        :param str source: The source code string from which to remove Java keywords.
        :return: The source code string with all Java keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Java.keywords_regex()), '', source).strip()
