import re
from PyReprism.utils import extension


class CSharp:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.csharp

    @staticmethod
    def keywords() -> list:
        keyword = 'abstract|add|alias|as|ascending|async|await|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|descending|do|double|dynamic|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|from|get|global|goto|group|if|implicit|in|int|interface|internal|into|is|join|let|lock|long|namespace|new|null|object|operator|orderby|out|override|params|partial|private|protected|public|readonly|ref|remove|return|sbyte|sealed|select|set|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|value|var|virtual|void|volatile|where|while|yield|warning|define|elif|endif|endregion|error|if|line|pragma|region|undef'.split('|')
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)f?')
        return pattern

    @staticmethod
    def operator_regex():
        pattern = re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/=?|%=?|\^=?|[?:~])')
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(CSharp.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C# boolean literals.

        This function generates a regular expression that matches the C# boolean literals `true`, `false`, and the special constant `null`.

        :return: A compiled regex pattern to match C# boolean literals and `null`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false|null)\b', re.IGNORECASE)

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C# delimiters.

        This function generates a regular expression that matches C# language delimiters, which include parentheses `()`, brackets `[]`, braces `{}`, commas `,`, colons `:`, periods `.`, semicolons `;`, at symbols `@`, angle brackets `<`, `>`, and the question mark `?`.

        :return: A compiled regex pattern to match C# delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>?]')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Python source code string.

        :param str source_code: The Python source code from which to remove comments.
        :param bool isList: (Optional) A flag indicating if the input is a list of source code lines. This parameter is not used in the function logic.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return CSharp.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in CSharp.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(CSharp.keywords_regex()), '', source)
