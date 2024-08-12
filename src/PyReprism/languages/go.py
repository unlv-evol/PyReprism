import re
from PyReprism.utils import extension


class Go:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.Go

    @staticmethod
    def keywords() -> list:
        keyword = 'break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go(?:to)?|if|import|interface|map|package|range|return|select|struct|switch|type|var|bool|byte|complex(?:64|128)|error|float32|float64|rune|string|u?int(?:8|16|32|64)?|uintptr|append|cap|close|complex|copy|delete|imag|len|make|new|panic|print|println|real|recover|iota|nil|true|false'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        pattern = re.compile(r'[*\/%^!=]=?|\+[=+]?|-[=-]?|\|[=|]?|&(?:=|&|\^=?)?|>(?:>=?|=)?|<(?:<=?|=|-)?|:=|\.\.\.')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(Go.keywords()) + r')\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Go delimiters.

        This function generates a regular expression that matches Go language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, and the ellipsis `...`.

        :return: A compiled regex pattern to match Go delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;]|\.{3}')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Go boolean literals.

        This function generates a regular expression that matches the Go boolean literals `true`, `false`, and the special constant `nil`.

        :return: A compiled regex pattern to match Go boolean literals and `nil`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|nil)\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Go source code string.

        :param str source_code: The Go source code from which to remove comments.
        :param bool isList: (Optional) A flag indicating if the input is a list of source code lines. This parameter is not used in the function logic.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Go.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Go.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Go.keywords_regex()), '', source)
