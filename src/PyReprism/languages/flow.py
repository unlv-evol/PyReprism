import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Flow(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.flow

    @classmethod
    def keywords(cls) -> list:
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>[^/\n]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        result = []
        for match in cls.comment_regex().finditer(source_code):
            non = match.groupdict().get('noncomment')
            if non:
                result.append(non)
        if isList:
            return result
        return ''.join(result)
