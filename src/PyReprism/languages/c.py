import re
from PyReprism.utils import extension


class C:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for C files.

        :return: The file extension for C files.
        :rtype: str
        """
        return extension.c

    @staticmethod
    def keywords() -> list:
        """
        Return a list of C keywords and built-in functions.

        :return: A list of C keywords and built-in function names.
        :rtype: list
        """
        keyword = '_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local|asm|typeof|inline|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|define|defined|elif|else|endif|error|ifdef|ifndef|if|import|include|line|pragma|undef|using|__FILE__|__LINE__|__DATE__|__TIME__|__TIMESTAMP__|__func__|EOF|NULL|SEEK_CUR|SEEK_END|SEEK_SET|stdin|stdout|stderr'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in C source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in C code.

        :return: A compiled regex pattern to match C numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C operators.

        :return: A compiled regex pattern to match various C operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'-[>-]?|\+\+?|!=?|<<?=?|>>?=?|==?|&&?|\|\|?|[~^%?*\/]')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C keywords.

        :return: A compiled regex pattern to match C keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(C.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C boolean literals.

        :return: A compiled regex pattern to match C boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C and C++ delimiters.

        :return: A compiled regex pattern to match C and C++ delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>*&]')

    @staticmethod
    def remove_comments(source_code: str) -> str:
        """
        Remove comments from the provided C source code string.

        :param str source_code: The C source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return C.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all C keywords from the provided source code string.

        :param str source: The source code string from which to remove C keywords.
        :return: The source code string with all C keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(C.keywords_regex()), '', source)
