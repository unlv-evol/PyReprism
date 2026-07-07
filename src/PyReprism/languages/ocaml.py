import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Ocaml(BaseLanguage):
    """OCaml support (``(* *)`` comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.ocaml

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'and|as|assert|begin|class|constraint|do|done|downto|else|end|exception|external|'
            'for|fun|function|functor|if|in|include|inherit|initializer|lazy|let|match|method|'
            'module|mutable|new|nonrec|object|of|open|or|private|rec|sig|struct|then|to|try|'
            'type|val|virtual|when|while|with|true|false'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>\(\*[\s\S]*?\*\))|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^(*"]*|[(*])',
            re.DOTALL | re.MULTILINE,
        )
