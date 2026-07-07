import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class TypeScript(BaseLanguage):
    """TypeScript language helper migrated to BaseLanguage."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.typescript

    @classmethod
    def keywords(cls) -> list:
        return 'as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|var|void|while|with|yield|module|declare|constructor|namespace|abstract|require|type|string|Function|any|number|boolean|Array|symbol|console'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Capture // and /* */ comments; preserve string literals in 'noncomment'.
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"\n]+)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/?=|%=?|\^=?|[?:~])')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false)\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Maintain original scalar behavior: substitution + strip.
        if isList:
            return super().remove_comments(source_code, isList=True)
        pattern = cls.comment_regex()
        return pattern.sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
