import re
from PyReprism.utils import extension


class Swift:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.swift

    @staticmethod
    def keywords() -> list:
        keyword = ''.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/\n]*[^\n]*)', re.DOTALL | re.MULTILINE)
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
        return re.compile(r'\b(' + '|'.join(Swift.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Swift boolean literals.

        This function generates a regular expression that matches the Swift boolean literals `true`, `false`, and the special constant `nil`.

        :return: A compiled regex pattern to match Swift boolean literals and `nil`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|nil)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Swift language delimiters.

        This function generates a regular expression that matches Swift language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, angle brackets `<`, `>`, the question mark `?`, and the exclamation mark `!`.

        :return: A compiled regex pattern to match Swift delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;<>?!]')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Rust source code string.

        :param str source_code: The Rust source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Swift.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Swift.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Swift.keywords_regex()), '', source)
