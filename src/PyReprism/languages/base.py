import re
from functools import lru_cache
from typing import List, Pattern, Union


class BaseLanguage:
    """Minimal base class for language implementations.

    Subclasses should provide: file_extension(), keywords(), comment_regex(),
    and may override number_regex(), operator_regex(), keywords_regex().

    This base centralizes implementations for remove_comments and remove_keywords
    and caches commonly used compiled regexes.
    """

    @classmethod
    def file_extension(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def keywords(cls) -> List[str]:
        return []

    @classmethod
    @lru_cache(maxsize=None)
    def keywords_regex(cls) -> Pattern:
        words = cls.keywords() or []
        if not words:
            # match nothing
            return re.compile(r"^$")
        return re.compile(r'\b(' + '|'.join(words) + r')\b', re.IGNORECASE)

    @classmethod
    def comment_regex(cls) -> Pattern:
        """Return a compiled regex that contains named groups 'comment' and 'noncomment'."""
        raise NotImplementedError()

    @classmethod
    def number_regex(cls) -> Pattern:
        return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> Pattern:
        return re.compile(r'.')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> Union[str, List[str]]:
        """Strip comments using the language's comment_regex.

        The regex is expected to provide a 'noncomment' named group for text to keep.
        Returns either the joined string or a list of non-comment segments when isList=True.
        """
        pattern = cls.comment_regex()
        result = []
        for match in pattern.finditer(source_code):
            non = match.groupdict().get('noncomment')
            # Append the 'noncomment' group even when it's an empty string.
            # Use `is not None` to avoid skipping valid empty segments which
            # may carry whitespace that should be preserved.
            if non is not None:
                result.append(non)
        if isList:
            return result
        return ''.join(result)

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(cls.keywords_regex(), '', source)
