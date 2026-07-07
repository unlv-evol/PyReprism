import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class PLSQL(BaseLanguage):
    """Oracle PL/SQL support (``--`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.plsql

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'BEGIN|END|DECLARE|PROCEDURE|FUNCTION|PACKAGE|BODY|TRIGGER|CURSOR|LOOP|WHILE|FOR|'
            'IF|ELSIF|ELSE|THEN|CASE|WHEN|EXIT|RETURN|EXCEPTION|RAISE|IS|AS|IN|OUT|NOCOPY|'
            'SELECT|INSERT|UPDATE|DELETE|MERGE|FROM|WHERE|INTO|VALUES|SET|AND|OR|NOT|NULL|'
            'TABLE|VIEW|INDEX|TYPE|RECORD|VARCHAR2|NUMBER|DATE|BOOLEAN|INTEGER|PLS_INTEGER|'
            'COMMIT|ROLLBACK|SAVEPOINT|GRANT|REVOKE|CREATE|REPLACE|DROP|ALTER'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>--.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>\'(\\.|\'\'|[^\'])*\'|.[^-/\']*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Case-insensitive keyword matcher.

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)
