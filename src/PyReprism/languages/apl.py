import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Apl(BaseLanguage):
    """APL language helper.

    This class provides minimal support for APL-like source files: file
    extension metadata, comment matching, and a conservative list of common
    APL primitives/operators for keyword removal. The keyword list is kept
    intentionally small; we can move to a data file later if you want a
    comprehensive set.
    """

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for APL files.

        :rtype: str
        """
        return extension.apl

    @classmethod
    def keywords(cls) -> list:
        """Return a conservative list of APL primitives and symbols.

        :rtype: list
        """
        # A conservative set of commonly-used APL symbols / primitives.
        return '⍝|⍴|⍳|⌈|⌊|⌿|⍟|∘|⍎|⍕'.split('|')

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex for APL line comments (started by '⍝').

        :rtype: re.Pattern
        """
        # APL uses the '⍝' glyph to start comments.
        return re.compile(r'(?P<comment>⍝.*?$)|(?P<noncomment>[^⍝]*)', re.MULTILINE)

    # Use BaseLanguage.number_regex and operator_regex by default.

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from APL source.

        :param source_code: the APL source text
        :type source_code: str
        :param isList: if True return list of non-comment fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        return super().remove_comments(source_code, isList=isList)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove known APL keywords from the source.

        :param source: input text
        :type source: str
        :rtype: str
        """
        return super().remove_keywords(source)
