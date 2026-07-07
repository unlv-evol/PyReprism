import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class NSIS(BaseLanguage):
    """NSIS installer script support (``;`` / ``#`` line and ``/* */`` block comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.nsis

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'Section|SectionEnd|SectionGroup|SectionGroupEnd|Function|FunctionEnd|'
            'Name|OutFile|InstallDir|Page|UninstPage|SetOutPath|File|WriteRegStr|'
            'WriteUninstaller|Delete|RMDir|CreateDirectory|CreateShortCut|MessageBox|'
            'Goto|Return|Call|Push|Pop|StrCmp|IntCmp|Abort|Quit|ExecWait|Exec'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>[;#].*?$|/\*.*?\*/)|'
            r'(?P<noncomment>"(\\.|[^\\"])*"|.[^;#/"]*)',
            re.DOTALL | re.MULTILINE,
        )
