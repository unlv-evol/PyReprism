import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class ActionScript(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for ActionScript files.

        :rtype: str
        """
        return extension.actionscript

    @classmethod
    def keywords(cls) -> list:
        """Return the list of ActionScript keywords and reserved words.

        :rtype: list
        """
        return 'as|break|case|catch|class|const|default|delete|do|else|extends|finally|for|function|if|implements|import|in|instanceof|interface|internal|is|native|new|null|package|private|protected|public|return|super|switch|this|throw|try|typeof|use|var|void|while|with|dynamic|each|final|get|include|namespace|native|override|set|static'.split('|')

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex that separates comments from non-comment code.

        The pattern provides a named capture group ``comment`` for comment
        fragments and ``noncomment`` for code fragments.

        :rtype: re.Pattern
        """
        # Keep the original pattern that captures // and /* */ comments and preserves non-comment sequences
        return re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return a regex that matches basic numeric literals.

        :rtype: re.Pattern
        """
        return re.compile(r'\b\d+\b')

    @classmethod
    def operator_regex(cls):
        """Return a regex for common ActionScript operators.

        :rtype: re.Pattern
        """
        return re.compile(r'\+\+|--|(?:[+\-*\/%^]|&&?|\|\|?|<<?|>>?>?|[!=]=?)=?|[~?@]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        """Remove comments from the provided ActionScript source.

        Delegates to :meth:`BaseLanguage.remove_comments` which uses the
        ``noncomment`` named group from :meth:`comment_regex` to assemble the
        non-comment fragments.

        :param source_code: the ActionScript source to strip comments from
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
        """Remove known ActionScript keywords from ``source`` using the compiled keywords regex.

        :param source: the source text to remove keywords from
        :type source: str
        :rtype: str
        """
        return re.sub(cls.keywords_regex(), '', source)
