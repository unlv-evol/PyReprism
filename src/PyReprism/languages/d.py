import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class D(BaseLanguage):
    """D language support (``//``, ``/* */`` and ``/+ +/`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.d

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'abstract|alias|align|asm|assert|auto|body|bool|break|byte|case|cast|catch|cdouble|'
            'cent|cfloat|char|class|const|continue|creal|dchar|debug|default|delegate|delete|'
            'deprecated|do|double|else|enum|export|extern|false|final|finally|float|for|foreach|'
            'foreach_reverse|function|goto|idouble|if|ifloat|immutable|import|inout|int|interface|'
            'invariant|ireal|lazy|long|macro|mixin|module|new|nothrow|null|out|override|package|'
            'pragma|private|protected|public|pure|real|ref|return|scope|shared|short|static|struct|'
            'super|switch|synchronized|template|this|throw|true|try|typedef|typeid|typeof|ubyte|'
            'ucent|uint|ulong|union|unittest|ushort|version|void|volatile|wchar|while|with|'
            'string|wstring|dstring|size_t|ptrdiff_t'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\+[\s\S]*?\+/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^/"]*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'\b0x\.?[a-f\d_]+(?:(?!\.\.)\.[a-f\d_]*)?(?:p[+-]?[a-f\d_]+)?[ulfi]*'
        )

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'\|[|=]?|&[&=]?|\+[+=]?|-[-=]?|\.?\.\.|=[>=]?|!(?:i[ns]\b|<>?=?|>=?|=)?|'
            r'\bi[ns]\b|(?:<[<>]?|>>?>?|\^\^|[*\/%^~])=?'
        )
