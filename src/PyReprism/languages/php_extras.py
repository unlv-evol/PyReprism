import re
from .php import PHP
from .registry import LanguageRegistry


@LanguageRegistry.register
class PHPExtras(PHP):
    """Alias/extension for PHP-related extras. Inherits behavior from PHP."""

    @classmethod
    def file_extension(cls) -> str:
        return PHP.file_extension()

    @classmethod
    def keywords(cls) -> list:
        # extend or reuse PHP keywords
        return PHP.keywords()
