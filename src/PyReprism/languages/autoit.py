import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Autoit(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.autoit

    @classmethod
    def keywords(cls) -> list:
        keyword = 'Case|Const|Continue(?:Case|Loop)|Default|Dim|Do|Else(?:If)?|End(?:Func|If|Select|Switch|With)|Enum|Exit(?:Loop)?|For|Func|Global|If|In|Local|Next|Null|ReDim|Select|Static|Step|Switch|Then|To|Until|Volatile|WEnd|While|With|True|False'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>;.*?$|#cs[\s\S]*?#ce|#cs.*?$|^.*?#ce)|(?P<noncomment>[^;#]*[^\n]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b(?:0x[\da-f]+|\d+(?:\.\d+)?(?:e[+-]?\d+)?)\b')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'<[=>]?|[-+*\/=&>]=?|[?^]|\b(?:And|Or|Not)\b')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        result = []
        for match in cls.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
