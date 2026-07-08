import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Eiffel(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.eiffel

    @classmethod
    def keywords(cls) -> list:
        keyword = 'across|agent|alias|all|and|attached|as|assign|attribute|check|class|convert|create|Current|debug|deferred|detachable|do|else|elseif|end|ensure|expanded|export|external|feature|from|frozen|if|implies|inherit|inspect|invariant|like|local|loop|not|note|obsolete|old|once|or|Precursor|redefine|rename|require|rescue|Result|retry|select|separate|some|then|undefine|until|variant|Void|when|xor|True|False'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        # Eiffel uses -- for line comments; strings are double-quoted.
        pattern = re.compile(r'(?P<comment>--.*?$)|(?P<noncomment>"[^"\n]*"|.[^"-]*)',
                             re.DOTALL | re.MULTILINE)
        return pattern

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0[xcb][\da-f](?:_*[\da-f])*\b|(?:\d(?:_*\d)*)?\.(?:(?:\d(?:_*\d)*)?e[+-]?)?\d(?:_*\d)*|\d(?:_*\d)*\.?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'\\\\|\|\.\.\||\.\.|\/[~\/=]?|[><]=?|[-+*^=~]')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
