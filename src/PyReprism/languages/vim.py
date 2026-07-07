import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Vim(BaseLanguage):
    """Vim script support (``"`` line comments)."""

    @classmethod
    def file_extension(cls) -> str:
        """:rtype: str"""
        return extension.vim

    @classmethod
    def keywords(cls) -> list:
        """:rtype: list[str]"""
        return (
            'function|endfunction|if|elseif|else|endif|while|endwhile|for|endfor|in|return|'
            'let|unlet|call|execute|echo|echom|set|setlocal|autocmd|augroup|command|'
            'try|catch|finally|endtry|throw|break|continue'
        ).split('|')

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        """:rtype: re.Pattern"""
        return re.compile(
            r'(?P<comment>".*?$)|(?P<noncomment>.[^"]*)',
            re.DOTALL | re.MULTILINE,
        )
