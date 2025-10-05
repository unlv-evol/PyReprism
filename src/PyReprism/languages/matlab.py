import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class MatLab(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.matlab

    @classmethod
    def keywords(cls) -> list:
        return 'break|case|catch|continue|else|elseif|end|for|function|if|inf|NaN|otherwise|parfor|pause|pi|return|switch|try|while'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>%\{[\s\S]*?\}%|%.*?$)|(?P<noncomment>[^%]*)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?(?:[ij])?|\b[ij]\b', re.IGNORECASE)

    @classmethod
    def operator_regex(cls):
        return re.compile(r"\.?[*^\/\\']|[+\-:@]|[<>=~]=?|&&?|\|\|?")

