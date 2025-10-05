import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Ada(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.ada

    @classmethod
    def keywords(cls) -> list:
        return 'abort|abs|abstract|accept|access|aliased|all|and|array|at|begin|body|case|constant|declare|delay|delta|digits|do|else|new|return|elsif|end|entry|exception|exit|for|function|generic|Adato|if|in|interface|is|limited|loop|mod|not|null|of|others|out|overriding|package|pragma|private|procedure|protected|raise|range|record|rem|renames|requeue|reverse|select|separate|some|subtype|synchronized|tagged|task|terminate|then|type|until|use|when|while|with|xor|true|false|null'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Ada uses '--' for single-line comments. Capture strings and non-comment segments.
        return re.compile(
            r"(?P<comment>--.*?$)|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|.[^-']*)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:0x[\da-f]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b', re.IGNORECASE)

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'[:=<>+\-*/&|^%]+')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
