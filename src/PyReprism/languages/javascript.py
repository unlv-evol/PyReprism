import re
from PyReprism.utils import extension


class JavaScript:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for JavaScript files.

        :return: The file extension for Java files.
        :rtype: str
        """
        return extension.javascript

    @staticmethod
    def keywords() -> list:
        """
        Return a list of JavaScript keywords and built-in functions.

        :return: A list of JavaScript keywords and built-in function names.
        :rtype: list
        """
        keyword = 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in JavaScript source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in JavaScript code.

        :return: A compiled regex pattern to match JavaScript numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'\b(?:0[xX][\dA-Fa-f]+|0[bB][01]+|0[oO][0-7]+|NaN|Infinity)\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee][+-]?\d+)?')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JavaScript operators.

        :return: A compiled regex pattern to match various JavaScript operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'-[-=]?|\+[+=]?|!=?=?|<<?=?|>>?>?=?|=(?:==?|>)?|&[&=]?|\|[|=]?|\*\*?=?|\/=?|~|\^=?|%=?|\?|\.{3}')
        return pattern

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JavaScript delimiters.

        This function generates a regular expression that matches JavaScript delimiters, including parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, at symbols `@`, as well as angle brackets `<` and `>`.

        :return: A compiled regex pattern to match JavaScript delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JavaScript keywords.

        :return: A compiled regex pattern to match JavaScript keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(JavaScript.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify JavaScript boolean literals.

        :return: A compiled regex pattern to match JavaScript boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false)\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided JavaScript source code string.

        :param str source_code: The JavaScript source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return JavaScript.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in JavaScript.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all JavaScript keywords from the provided source code string.

        :param str source: The source code string from which to remove JavaScript keywords.
        :return: The source code string with all JavaScript keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(JavaScript.keywords_regex()), '', source)
