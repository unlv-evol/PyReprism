import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Bro(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.bro

    @classmethod
    def keywords(cls) -> list:
        # Conservative, common Bro/Zeek keywords and types
        return [
            'break','next','continue','alarm','using','of','add','delete','export','print','return','schedule','when','timeout',
            'addr','any','bool','count','double','enum','file','int','interval','pattern','opaque','port','record','set','string','subnet','table','time','vector',
            'for','if','else','in','module','function','load','unload','prefixes','ifdef','ifndef','DIR','FILENAME','redef','priority','log','optional','default'
        ]

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>.[^#]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\da-fA-F]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&|\|\|?|\?|\*|\/|~|\^|%')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(re.escape(k) for k in cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
