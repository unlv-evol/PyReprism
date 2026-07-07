import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class NIM(BaseLanguage):
    """Nim language support (``#`` line and ``#[ ]#`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.nim

    @classmethod
    def keywords(cls) -> list:
        return (
            'addr|and|as|asm|bind|block|break|case|cast|concept|const|continue|converter|'
            'defer|discard|distinct|div|do|elif|else|end|enum|except|export|finally|for|from|'
            'func|if|import|in|include|interface|is|isnot|iterator|let|macro|method|mixin|mod|'
            'nil|not|notin|object|of|or|out|proc|ptr|raise|ref|return|shl|shr|static|template|'
            'try|tuple|type|using|var|when|while|xor|yield|true|false|result|echo'
        ).split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#\[[\s\S]*?\]#|#.*?$)|(?P<noncomment>"(\\.|[^\\"])*"|.[^#"]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/?=|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:')

    @classmethod
    def keywords_regex(cls):
        keys = cls.keywords()
        if not keys:
            return re.compile(r'$^')
        return re.compile(r'\b(' + '|'.join(re.escape(k) for k in keys) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        kr = cls.keywords_regex()
        if kr.pattern == '$^':
            return source
        return re.sub(kr, '', source)