import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Docker(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.docker

    @classmethod
    def keywords(cls) -> list:
        keyword = 'ADD|ARG|CMD|COPY|ENTRYPOINT|ENV|EXPOSE|FROM|HEALTHCHECK|LABEL|MAINTAINER|ONBUILD|RUN|SHELL|STOPSIGNAL|USER|VOLUME|WORKDIR'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#]*)', re.MULTILINE)
        return pattern

    @classmethod
    def number_regex(cls):
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(re.compile(cls.keywords_regex()), '', source)
