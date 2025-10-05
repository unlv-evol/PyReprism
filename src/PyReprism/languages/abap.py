import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Abap(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.abap

    @classmethod
    def keywords(cls) -> list:
        # Keep keywords minimal for now to avoid a huge inline list.
        # The original project had a very large set; add more to data/ later.
        return []

    @classmethod
    def comment_regex(cls):
        # Preserve original matching behavior: lines starting with *,
        # double-quote inline comments, and (* ... *) block comments.
        return re.compile(
            r'''(?P<comment>^\*.*?$|".*?$|\(\*[\s\S]*?\*\)|\(\*.*?$|^.*?\*\))|(?P<noncomment>'(\\.|[^\\'])*'|"(\\.|[^\\"])*"|.[^*"']*)''',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls):
        return re.compile(r"\b\d+\b")

    @classmethod
    def operator_regex(cls):
        return re.compile(r"(\s)(?:\*\*?|<[=>]?|>=?|\?=|[-+\/=])(?=\s)")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Delegate to BaseLanguage which uses the 'noncomment' group.
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
