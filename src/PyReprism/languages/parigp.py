import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class PariGP(BaseLanguage):
    r"""PARI/GP support (``\\`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.parigp

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'breakpoint|break|dbg_down|dbg_err|dbg_up|dbg_x|forcomposite|fordiv|forell|'
            'forpart|forprime|forstep|forsubgroup|forvec|for|if|iferr|next|return|until|while'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        r""":rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>\\\\.*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^\\/"]*)',
            re.DOTALL | re.MULTILINE,
        )
