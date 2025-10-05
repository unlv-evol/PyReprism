import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class AppleScript(BaseLanguage):
    """AppleScript language helper.

    Provides file extension metadata, comment/number/operator regexes, and a
    conservative keywords list for AppleScript. The comment matching supports
    single-line comments starting with `--` or `#` and block comments using
    `(* ... *)`.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.applescript

    @classmethod
    def keywords(cls) -> list:
        # A conservative (cleaned) set of AppleScript keywords and types. This
        # can be extended or moved to a data file if you want the complete set.
        kw = (
            'about|above|after|against|around|aside from|at|back|before|beginning|behind|below|'
            'beneath|beside|between|but|by|continue|copy|does|else|end|error|every|exit|false|'
            'first|for|from|get|global|if|in|into|is|it|its|last|local|me|my|of|on|out|over|prop|'
            'property|put|repeat|return|set|since|some|tell|that|the|then|through|to|true|try|until|'
            'where|while|with|without|alias|application|boolean|class|constant|date|file|integer|list|'
            'number|real|record|reference|script|text|centimetres|centimeters|feet|inches|kilometres|'
            'kilometers|metres|meters|miles|yards|square|cubic|gallons|litres|liters|quarts|grams|'
            'kilograms|ounces|pounds|degrees|Celsius|Fahrenheit|Kelvin'
        )
        return kw.split('|')

    @classmethod
    def comment_regex(cls):
        # Support: -- comment, # comment, and block comments (* ... *)
        return re.compile(r'(?P<comment>--.*?$|#.*?$|\(\*[\s\S]*?\*\))|(?P<noncomment>[^#\-\(\*)]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?\b')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'[&=≠≤≥*+\-/÷^]|[<>]=?')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return super().remove_keywords(source)
