import re
from PyReprism.utils import extension


class Kotlin:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.kotlin

    @staticmethod
    def keywords() -> list:
        keyword = 'abstract|annotation|as|break|by|catch|class|companion|const|constructor|continue|crossinline|data|do|else|enum|final|finally|for|fun|get|if|import|in|init|inline|inner|interface|internal|is|lateinit|noinline|null|object|open|out|override|package|private|protected|public|reified|return|sealed|set|super|tailrec|this|throw|to|try|val|var|when|where|while'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'\b(?:0[bx][\da-fA-F]+|\d+(?:\.\d+)?(?:e[+-]?\d+)?[fFL]?)\b')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        pattern = re.compile(r'+[+=]?|-[-=>]?|==?=?|!(?:!|==?)?|[\/*%<>]=?|[?:]:?|\.\.|&&|\|\||\b(?:and|inv|or|shl|shr|ushr|xor)\b')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(Kotlin.keywords()) + r')\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Kotlin language delimiters.

        This function generates a regular expression that matches Kotlin language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, angle brackets `<`, `>`, and the question mark `?`.

        :return: A compiled regex pattern to match Kotlin delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;<>?]')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Kotlin boolean literals.

        This function generates a regular expression that matches the Kotlin boolean literals `true`, `false`, and the special constant `null`.

        :return: A compiled regex pattern to match Kotlin boolean literals and `null`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|null)\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Kotlin source code string.

        :param str source_code: The Kotlin source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Kotlin.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Kotlin.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Kotlin.keywords_regex()), '', source)
