import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Dart(BaseLanguage):
    """Dart language helper migrated to BaseLanguage pattern."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.dart

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|assert|async|await|break|case|catch|class|const|continue|default|deferred|do|dynamic|else|enum|export|external|extends|factory|final|finally|for|get|if|implements|import|in|library|new|null|operator|part|rethrow|return|set|static|super|switch|this|throw|try|typedef|var|void|while|with|yield|sync'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Safe comment regex: capture C-style block comments and line comments
        # in the 'comment' group and string/non-comment fragments in 'noncomment'.
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"\n]+)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'\bis!|\b(?:as|is)\b|\+\+|--|&&|\|\||<<=?|>>=?|~(?:/=?)?|[+\-*/%&^|=!<>]=?|\?')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;<>]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|null)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve original scalar behavior: substitution + strip.
        if isList:
            return super().remove_comments(source_code, isList=True)
        pattern = cls.comment_regex()
        return pattern.sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
