import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Abap(BaseLanguage):
    """ABAP language adapter.

    Provides basic patterns for comment removal and simple token matching.
    This implementation intentionally keeps the keyword list minimal; a
    more complete list can be provided later from a data file.
    """

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for ABAP files.

        :rtype: str
        """
        return extension.abap

    @classmethod
    def keywords(cls) -> list:
        """Return a (possibly empty) list of ABAP keywords.

        Keep this minimal to avoid large inline lists in the source. A fuller
        list can be loaded from a data file if needed.

        :rtype: list
        """
        return []

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """Compile and return a regex that separates comments from code.

        The pattern provides a named capture group ``comment`` for comment
        fragments and ``noncomment`` for code fragments. ``BaseLanguage.remove_comments``
        expects the ``noncomment`` group to extract non-comment content.

        ABAP comment forms handled:
        - Lines that start with an asterisk (*...)
        - Inline comments that start with a double-quote (")
        - Block comments using (* ... *)

        :rtype: re.Pattern
        """
        return re.compile(
            r'''(?P<comment>^\*.*?$|".*?$|\(\*[\s\S]*?\*\)|\(\*.*?$|^.*?\*\))|(?P<noncomment>'(\\.|[^\\'])*'|"(\\.|[^\\"])*"|.[^*"']*)''',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """Return a regex matching integer-like numbers in ABAP source.

        :rtype: re.Pattern
        """
        return re.compile(r"\b\d+\b")

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        """Return a regex for ABAP operators (basic/heuristic).

        :rtype: re.Pattern
        """
        return re.compile(r"(\s)(?:\*\*?|<[=>]?|>=?|\?=|[-+\\/=])(?=\s)")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from ABAP source.

        Delegates to :meth:`BaseLanguage.remove_comments`, which uses the
        ``noncomment`` named group from :meth:`comment_regex` to build the result.

        :param source_code: the ABAP source to strip comments from
        :type source_code: str
        :param isList: if True return a list of non-comment fragments; otherwise
            return a single trimmed string
        :type isList: bool
        :rtype: list[str] or str
        """
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return res.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        """Remove known ABAP keywords from ``source`` using the compiled keywords regex.

        :param source: the source text to remove keywords from
        :type source: str
        :rtype: str
        """
        return re.sub(cls.keywords_regex(), '', source)
