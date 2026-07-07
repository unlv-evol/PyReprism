import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Vbnet(BaseLanguage):
    """VB.NET support (``'`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.vbnet

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'AddHandler|AddressOf|Alias|And|AndAlso|As|Boolean|ByRef|Byte|ByVal|Call|Case|Catch|'
            'Class|Const|Continue|Date|Decimal|Declare|Default|Delegate|Dim|DirectCast|Do|Double|'
            'Each|Else|ElseIf|End|EndIf|Enum|Erase|Error|Event|Exit|Finally|For|Friend|Function|'
            'Get|GetType|GoTo|Handles|If|Implements|Imports|In|Inherits|Integer|Interface|Is|'
            'Let|Lib|Like|Long|Loop|Me|Mod|Module|MustInherit|MustOverride|MyBase|MyClass|'
            'Namespace|New|Next|Not|Nothing|Object|Of|On|Operator|Option|Optional|Or|OrElse|'
            'Overloads|Overridable|Overrides|ParamArray|Partial|Private|Property|Protected|'
            'Public|RaiseEvent|ReadOnly|ReDim|RemoveHandler|Resume|Return|Select|Set|Shadows|'
            'Shared|Short|Single|Static|Step|Stop|String|Structure|Sub|SyncLock|Then|Throw|To|'
            'Try|TypeOf|Until|Variant|Wend|When|While|With|WithEvents|WriteOnly|Xor|True|False'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>\'.*?$)|(?P<noncomment>.[^\']*)',
            re.DOTALL | re.MULTILINE,
        )

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(r'[()\[\]{}.,:;<>&]')

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(r'\b(?:True|False|Nothing)\b', re.IGNORECASE)

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        """Case-insensitive keyword matcher (VB.NET is case-insensitive).

        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b', re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Strip VB.NET comments.

        :param source_code: The VB.NET source to process.
        :param isList: If True, return a list of non-comment segments.
        :rtype: str or list[str]
        """
        if isList:
            return super().remove_comments(source_code, isList=True)
        return super().remove_comments(source_code).strip()
