import re
from PyReprism.utils import extension


class Rust:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.rust

    @staticmethod
    def keywords() -> list:
        keyword = 'abstract|alignof|as|be|box|break|const|continue|crate|do|else|enum|extern|false|final|fn|for|if|impl|in|let|loop|match|mod|move|mut|offsetof|once|override|priv|pub|pure|ref|return|sizeof|static|self|struct|super|true|trait|type|typeof|unsafe|unsized|use|virtual|where|while|yield'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>//.*?$|///.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'\b(?:0x[\dA-Fa-f](?:_?[\dA-Fa-f])*|0o[0-7](?:_?[0-7])*|0b[01](?:_?[01])*|(\d(?:_?\d)*)?\.?\d(?:_?\d)*(?:[Ee][+-]?\d+)?)(?:_?(?:[iu](?:8|16|32|64)?|f32|f64))?\b')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        pattern = re.compile(r'[-+*\/%!^]=?|=[=>]?|@|&[&=]?|\|[|=]?|<<?=?|>>?=?')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(Rust.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Rust boolean literals.

        This function generates a regular expression that matches the Rust boolean literals `true`, `false`, and the special constant `None`.

        :return: A compiled regex pattern to match Rust boolean literals and `None`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|None)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Rust language delimiters.

        This function generates a regular expression that matches Rust language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, angle brackets `<`, `>`, and the question mark `?`.

        :return: A compiled regex pattern to match Rust delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;<>?]')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Rust source code string.

        :param str source_code: The Rust source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Rust.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Rust.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Rust.keywords_regex()), '', source)
