import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Groovy(BaseLanguage):
    """Groovy language helper."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.groovy

    @classmethod
    def keywords(cls) -> list:
        return 'as|def|in|abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|trait|transient|try|void|volatile|while|setup|given|when|then|and|cleanup|expect|where'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Safer, simpler pattern: match // line comments and /* */ block comments
        # and treat quoted strings as noncomment segments.
        return re.compile(
            r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|"
            r"(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\n'\"]+)",
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:0b[01_]+|0x[\da-f_]+(?:\.[\da-f_p\-]+)?|[\d_]+(?:\.[\d_]+)?(?:e[+-]?[\d]+)?)[glidf]?\b')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(^|[^.])(?:~|==?~?|\?[.:]?|\*(?:[.=]|\*=?)?|\.[@&]|\.\.<|\.{1,2}(?!\.)|-[-=>]?|\+[+=]?|!=?|<(?:<=?|=>?)?|>(?:>>?=?|=)?|&[&=]?|\|[|=]?|\/?=?|\^=?|%=?)')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        result = []
        for match in cls.comment_regex().finditer(source_code):
            non = match.groupdict().get('noncomment')
            if non:
                result.append(non)
        if isList:
            return result
        return ''.join(result)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
