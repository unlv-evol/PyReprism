import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Java(BaseLanguage):
    """Java language helper; migrated to BaseLanguage pattern.

    Provides regex helpers and delegates comment/keyword removal to BaseLanguage.
    """

    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for Java files.
        :rtype: str
        """
        return extension.java

    @classmethod
    def keywords(cls) -> list:
        """Return a list of Java keywords and built-in functions.
        :rtype: list[str]
        """
        return 'abstract|continue|for|new|switch|assert|default|goto|package|synchronized|boolean|do|if|private|this|break|double|implements|protected|throw|byte|else|import|public|throws|case|enum|instanceof|return|transient|catch|extends|int|short|try|char|final|interface|static|void|class|finally|long|strictfp|volatile|const|float|native|super|while'.split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """Regex to capture comments (group 'comment') and non-comment fragments (group 'noncomment').

        :rtype: re.Pattern
        """
        return re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        """Regex for numeric literals.
        
        :rtype: re.Pattern
        """
        return re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?[df]?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        """Regex for Java operators.
    
        :rtype: re.Pattern
        """
        return re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/?=|%=?|\^=?|[?:~])')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Compile and return a regex that matches Java keywords.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        """Regex for Java boolean literals.

        :param source: The source code string from which to remove Java keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:true|false)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        """Regex for Java delimiters.

        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Preserve original Java behavior: for scalar output perform a
        substitution then strip (as older implementation did). If the
        caller requests a list, fall back to BaseLanguage's behavior.

        :param source_code: The Java source code to process.
        :param isList: If True, return a list of non-comment segments; otherwise, return a single string.
        :rtype: str or list[str]    
        """
        if isList:
            return super().remove_comments(source_code, isList=True)
        pattern = cls.comment_regex()
        # replicate original substitution behavior then strip the result
        return pattern.sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        """Delegate keyword removal to BaseLanguage.

        :param source: The source code string from which to remove Java keywords.
        :rtype: str
        """
        return super().remove_keywords(source)
