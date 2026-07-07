import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Clojure(BaseLanguage):
    """Clojure language adapter implementing the BaseLanguage contract.

    This implementation provides a conservative set of core forms,
    comment handling, and simple numeric/keyword patterns.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.clojure

    @classmethod
    def keywords(cls) -> list:
        # A conservative set of core Clojure forms and special symbols
        return [
            'def', 'defn', 'if', 'do', 'let', 'quote', 'var', 'fn', 'loop', 'recur',
            'throw', 'try', 'monitor-enter', 'new', 'set!', 'defmacro', 'defmulti',
            'defmethod', 'defstruct', 'defonce', 'declare', 'true', 'false', 'nil',
            'and', 'or', 'not', 'first', 'rest', 'cons', 'conj', 'map', 'filter',
            'reduce', 'apply', 'seq', 'concat', '->', '->>', 'when', 'when-not',
            'doseq', 'dotimes', 'for'
        ]

    @classmethod
    def comment_regex(cls):
        # semicolon begins a line or inline comment in Clojure
        return re.compile(r'(?P<comment>;.*?$)|(?P<noncomment>[^;\n].*?$)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b\d+(?:\.\d+)?\b')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(re.escape(k) for k in cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
