import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Docker(BaseLanguage):
    """Dockerfile language helper.

    Provides comment removal for Dockerfiles (lines starting with ``#``), a
    basic keywords list for common Dockerfile directives, and simple regexes
    for numbers and operators used by normalization utilities.
    """

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension/name used for Dockerfiles.

        Dockerfiles are often named "Dockerfile" rather than by extension,
        but we keep the canonical name from the project's extensions map.

        :rtype: str
        """
        return extension.docker

    @classmethod
    def keywords(cls) -> list:
        """Return Dockerfile directive keywords used for token filtering.

        :rtype: list
        """
        keyword = 'ADD|ARG|CMD|COPY|ENTRYPOINT|ENV|EXPOSE|FROM|HEALTHCHECK|LABEL|MAINTAINER|ONBUILD|RUN|SHELL|STOPSIGNAL|USER|VOLUME|WORKDIR'.split('|')
        return keyword

    @classmethod
    def comment_regex(cls):
        """Return a regex capturing Dockerfile comments and non-comment text.

        Matches lines starting with ``#`` as comments. The compiled pattern
        provides named groups ``comment`` and ``noncomment`` required by
        BaseLanguage.remove_comments.

        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]+)', re.MULTILINE)
        return pattern

    @classmethod
    def number_regex(cls):
        """Return a regex matching numeric literals (heuristic).

        Dockerfiles commonly contain ports and numeric arguments; this
        pattern is intentionally simple.

        :rtype: re.Pattern
        """
        return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

    @classmethod
    def operator_regex(cls):
        """Return a regex matching simple operators and punctuation.

        This is used for token splitting during normalization.

        :rtype: re.Pattern
        """
        return re.compile(r'[=+\-*/<>!&|%:]+')

    @classmethod
    def keywords_regex(cls):
        """Compile a regex that matches any Dockerfile directive keyword.

        :rtype: re.Pattern
        """
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from Dockerfile source.

        :param source_code: Dockerfile source text
        :type source_code: str
        :param isList: when True return list of non-comment fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove known Dockerfile directive keywords from source.

        Delegates to BaseLanguage.remove_keywords which uses the
        cached keywords_regex implementation.

        :param source: input source text
        :type source: str
        :rtype: str
        """
        return super().remove_keywords(source)
