import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry

@LanguageRegistry.register
class NIX(BaseLanguage):
    """Nix language minimal support.
    Handles line-oriented comments (lines starting with #) vs non-comment lines.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.nix

    @classmethod
    def keywords(cls) -> list:
        return 'let|in|if|then|else|rec|with|inherit|assert|or|and|import|abort|baseNameOf|dirOf|builtins'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>^#.*?$)|(?P<noncomment>^[^#\n].*?$)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'\b0x[\dA-Fa-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/?=|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)