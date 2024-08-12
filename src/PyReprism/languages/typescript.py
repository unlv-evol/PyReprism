import re
from PyReprism.utils import extension


class TypeScript:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.typescript

    @staticmethod
    def keywords() -> list:
        keyword = 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield|module|declare|constructor|namespace|abstract|require|type|string|Function|any|number|boolean|Array|symbol|console'.split('|')
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/|/\*\*[\s\S]*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')
        return pattern

    @staticmethod
    def operator_regex():
        pattern = re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/=?|%=?|\^=?|[?:~])')
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(TypeScript.keywords()) + r')\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify TypeScript delimiters.

        This function generates a regular expression that matches TypeScript delimiters, including parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, at symbols `@`, as well as angle brackets `<` and `>`.

        :return: A compiled regex pattern to match TypeScript delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify TypeScript boolean literals.

        :return: A compiled regex pattern to match TypeScript boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false)\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided TypeScript source code string.

        :param str source_code: The TypeScript source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return TypeScript.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in TypeScript.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(TypeScript.keywords_regex()), '', source)
