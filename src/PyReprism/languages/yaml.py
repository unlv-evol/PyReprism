import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Yaml(BaseLanguage):
    """YAML support (``#`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.yaml

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return ['true', 'false', 'null', 'yes', 'no', 'on', 'off']

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # A # starts a comment only after whitespace; quoted scalars are kept whole.
        return re.compile(
            r"(?P<comment>(?:^|(?<=[ \t]))#.*?$)|(?P<noncomment>(?:(?<=[\s:,\[{-])|^)(?:\"(?:\\.|[^\\\"\n])*\"|'(?:''|[^'\n])*')|.[^#\"'\n]*|.)",
            re.DOTALL | re.MULTILINE)
