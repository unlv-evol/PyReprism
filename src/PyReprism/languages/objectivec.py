import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class ObjectiveC(BaseLanguage):
    """Objective-C language helpers (minimal migration to BaseLanguage).

    Preserves the original comment-removal semantics (scalar vs list) and
    provides compiled regex helpers for numbers/operators/delimiters.
    """

    @classmethod
    def file_extension(cls) -> str:
        return extension.objectivec

    @classmethod
    def keywords(cls) -> list:
        # Keep C-family keywords; Objective-C @-directives are not suitable
        # for word-boundary keyword removal (they include the '@' prefix).
        return 'asm|typeof|inline|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|in|self|super'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Capture // line comments and C-style block comments; provide a
        # 'noncomment' group with the text to keep.
        return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>"(\\.|[^\\"])*"|.[^/"]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*', re.IGNORECASE)

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'-[->]?|\+\+?|!=?|<<?=?|>>?=?|==?|&&?|\|\|?|[~^%?*\/@]')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve original behavior: only append non-empty noncomment groups.
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
        return re.sub(cls.keywords_regex(), '', source)
