import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class CoffeeScript(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.coffeescript

    @classmethod
    def keywords(cls) -> list:
        keyword = 'and|break|by|catch|class|continue|debugger|delete|do|each|else|extend|extends|false|finally|for|if|in|instanceof|is|isnt|let|loop|namespace|new|no|not|null|of|off|on|or|own|return|super|switch|then|this|throw|true|try|typeof|undefined|unless|until|when|while|window|with|yes|yield'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>#.*?$|###.*?###)|(?P<noncomment>[^#\n].*?$)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(re.escape(k) for k in cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
