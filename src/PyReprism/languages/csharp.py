import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class CSharp(BaseLanguage):
    """C# language helper."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.csharp

    @classmethod
    def keywords(cls) -> list:
        return 'abstract|add|alias|as|ascending|async|await|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|descending|do|double|dynamic|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|from|get|global|goto|group|if|implicit|in|int|interface|internal|into|is|join|let|lock|long|namespace|new|null|object|operator|orderby|out|override|params|partial|private|protected|public|readonly|ref|remove|return|sbyte|sealed|select|set|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|value|var|virtual|void|volatile|where|while|yield|warning|define|elif|endif|endregion|error|if|line|pragma|region|undef'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\n'\"]+)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)f?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/?=|%=?|\^=?|[?:~])')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:true|false|null)\b', re.IGNORECASE)

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@<>?]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve legacy scalar behavior: substitution + strip
        out = cls.comment_regex().sub(lambda m: m.groupdict().get('noncomment') or '', source_code).strip()
        if isList:
            return [out]
        return out

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
