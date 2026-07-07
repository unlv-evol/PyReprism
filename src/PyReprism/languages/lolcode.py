import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class LOLCODE(BaseLanguage):
    """LOLCODE language minimal support.
    Handles line-oriented comments (lines starting with BTW) and block comments (OBTW ... TLDR).
    """
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension for LOLCODE source files.

        :rtype: str
        """
        return extension.lolcode

    @classmethod
    def keywords(cls) -> list:
        """Return a conservative list of LOLCODE keywords.
        
        :rtype: list"""
        return r'HAI|KTHXBYE|CAN HAS|I HAS A|ITZ|R|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ALL OF|ANY OF|O RLY\?|YA RLY|MEBBE|NO WAI|OIC|MKIH|RLY\?|WTF\?|OMG|OMGWTF|GTFO'.split('|')

    @classmethod
    def comment_regex(cls):
        """Return a regex capturing LOLCODE comments and non-comment fragments.

        Supports line comments starting with BTW and block comments between OBTW and TLDR.

        :rtype: re.Pattern
        """
        return re.compile(r'(?P<comment>BTW.*?$|OBTW[\s\S]*?TLDR)|(?P<noncomment>[^B]*(?:B(?!T(?:W|\s*TW))[^B]*)*)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return a regex capturing LOLCODE numeric literals.

        :rtype: re.Pattern
        """
        return re.compile(r'\b-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?\b')

    @classmethod
    def operator_regex(cls):
        """Return a regex matching common LOLCODE operators.
        
        :rtype: re.Pattern
        """
        return re.compile(r'\+|\-|\*|\/|%|\^|!|&&?|\|\|?')

    @classmethod
    def keywords_regex(cls):
        """Return a regex matching LOLCODE keywords.
        
        :rtype: re.Pattern
        """
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        """Remove comments from the given LOLCODE source code. 

        :param source_code: The LOLCODE source code to process.
        :param isList: If True, return a list of non-comment segments; otherwise, return a single string.   
        :rtype: str or list[str]    
        """
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return ''.join(res)