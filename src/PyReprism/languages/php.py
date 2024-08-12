import re
from PyReprism.utils import extension


class PHP:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for PHP files.

        :return: The file extension for PHP files.
        :rtype: str
        """
        return extension.php

    @staticmethod
    def keywords() -> list:
        """
        Return a list of PHP keywords and built-in functions.

        :return: A list of PHP keywords and built-in function names.
        :rtype: list
        """
        keyword = 'and|or|xor|array|as|break|case|cfunction|class|const|continue|declare|default|die|do|else|elseif|enddeclare|endfor|endforeach|endif|endswitch|endwhile|extends|for|foreach|function|include|include_once|global|if|new|return|static|switch|use|require|require_once|var|while|abstract|interface|public|implements|private|protected|parent|throw|null|echo|print|trait|namespace|final|yield|goto|instanceof|finally|try|catch'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in PHP source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>#.*?$|//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in PHP code.

        :return: A compiled regex pattern to match PHP numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[bo])?(?:(?:\d|0x[\da-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b', re.IGNORECASE)
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify PHP operators.

        :return: A compiled regex pattern to match various PHP operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]|\b(?:or|and|not)\b')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify PHP keywords.

        :return: A compiled regex pattern to match PHP keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(PHP.keywords()) + r')\b', re.IGNORECASE)

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify PHP delimiters.

        This function generates a regular expression that matches PHP delimiters, including parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, at symbols `@`, angle brackets `<` and `>`, as well as PHP-specific tokens like `$` for variables.

        :return: A compiled regex pattern to match PHP delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>$]')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify PHP boolean literals.

        This function generates a regular expression that matches the PHP boolean literals `true`, `false`, and the special constant `null`. The matching is case-insensitive, as PHP boolean literals are not case-sensitive.

        :return: A compiled regex pattern to match PHP boolean literals and `null`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|null)\b', re.IGNORECASE)

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided PHP source code string.

        :param str source_code: The PHP source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return PHP.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in PHP.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all PHP keywords from the provided source code string.

        :param str source: The source code string from which to remove PHP keywords.
        :return: The source code string with all PHP keywords removed.
        :rtype
        """
        return re.sub(re.compile(PHP.keywords_regex()), '', source)
