import re
from PyReprism.utils import extension


class CPP:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for C++ files.

        :return: The file extension for C++ files.
        :rtype: str
        """
        return extension.cpp

    @staticmethod
    def keywords() -> list:
        """
        Return a list of C++ keywords and built-in functions.

        :return: A list of C++ keywords and built-in function names.
        :rtype: list
        """
        keyword = 'alignas|alignof|asm|auto|bool|break|case|catch|char|char16_t|char32_t|class|compl|const|constexpr|const_cast|continue|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|extern|float|for|friend|goto|if|inline|int|int8_t|int16_t|int32_t|int64_t|uint8_t|uint16_t|uint32_t|uint64_t|long|mutable|namespace|new|noexcept|nullptr|operator|private|protected|public|register|reinterpret_cast|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|true|false'.split('|')
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
        Compile and return a regular expression pattern to identify numeric literals in C++ code.

        :return: A compiled regex pattern to match C++ numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C++ operators.

        :return: A compiled regex pattern to match various C++ operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'--?|\+\+?|!=?|<{1,2}=?|>{1,2}=?|->|:{1,2}|={1,2}|\^|~|%|&{1,2}|\|\|?|\?|\*|\/|\b(?:and|and_eq|bitand|bitor|not|not_eq|or|or_eq|xor|xor_eq)\b')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Return a list of C++ keywords and built-in functions.

        :return: A list of C++ keywords and built-in function names.
        :rtype: list
        """
        return re.compile(r'\b(' + '|'.join(CPP.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify C++ boolean literals.

        :return: A compiled regex pattern to match C++ boolean literals.
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
        Remove comments from the provided C++ source code string.

        :param str source_code: The C++ source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return CPP.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all C++ keywords from the provided source code string.

        :param str source: The source code string from which to remove C++ keywords.
        :return: The source code string with all C++ keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(CPP.keywords_regex()), '', source)
