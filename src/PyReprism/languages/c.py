import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class C(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.c

    @classmethod
    def keywords(cls) -> list:
        return '_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local|asm|typeof|inline|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|define|defined|elif|else|endif|error|ifdef|ifndef|if|import|include|line|pragma|undef|using|__FILE__|__LINE__|__DATE__|__TIME__|__TIMESTAMP__|__func__|EOF|NULL|SEEK_CUR|SEEK_END|SEEK_SET|stdin|stdout|stderr'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """
        Returns a compiled regex pattern to match comments and non-comment parts in C source code.
        This pattern matches both single-line (//) and multi-line (/* ... */) comments

        :returns: A compiled regex pattern.
        :type: re.Pattern
        """
        return re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """
        Returns a compiled regex pattern to match numeric literals in C source code.
        This pattern matches hexadecimal, decimal, and floating-point numbers
        
        :returns: A compiled regex pattern.
        :type: re.Pattern
        """
        return re.compile(r'(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        """
        Returns a compiled regex pattern to match operators in C source code.
        This pattern matches various C operators including arithmetic, comparison, and logical operators.   
        
        :returns: A compiled regex pattern.
        :type: re.Pattern
        """
        return re.compile(r'-[>-]?|\+\+?|!=?|<<?=?|>>?=?|==?|&&?|\|\|?|[~^%?*\/]')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@<>*&]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
