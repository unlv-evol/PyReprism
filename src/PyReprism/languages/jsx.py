import re
from PyReprism.utils import extension


class Jsx:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for JSX files.

        :return: The file extension for JSX files.
        :rtype: str
        """
        return extension.jsx

    @staticmethod
    def keywords() -> list:
        """
        Return a list of JSX keywords and built-in functions.

        :return: A list of JSX keywords and built-in function names.
        :rtype: list
        """
        keyword = 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in JSX source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|\{/\*[\s\S]*?\*/\}|/\*.*?$|^.*?\*/|/\*\*[\s\S]*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in JSX code.

        :return: A compiled regex pattern to match JSX numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'\b(?:0[xX][\dA-Fa-f]+|0[bB][01]+|0[oO][0-7]+|NaN|Infinity)\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][+-]?\d+)?')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JSX operators.

        :return: A compiled regex pattern to match various JSX operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'-[-=]?|\+[+=]?|!=?=?|<<?=?|>>?>?=?|=(?:==?|>)?|&[&=]?|\|[|=]?|\*\*?=?|\/=?|~|\^=?|%=?|\?|\.{3}')
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Jsx.keywords()) + r')\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JSX delimiters.

        This function generates a regular expression that matches JSX delimiters, including parentheses `(`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, at symbols `@`, as well as angle brackets `<` and `>`.

        :return: A compiled regex pattern to match JSX delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JSX boolean literals.

        :return: A compiled regex pattern to match JSX boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|null)\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided JSX source code string.

        :param str source_code: The JSX source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        result = []
        for match in Jsx.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all JSX keywords from the provided source code string.

        :param str source: The source code string from which to remove JSX keywords.
        :return: The source code string with all JSX keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Jsx.keywords_regex()), '', source)
