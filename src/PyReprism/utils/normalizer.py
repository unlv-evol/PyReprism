import re


class Normalizer:
    """Static helpers for normalizing whitespace in source code."""

    @staticmethod
    def whitespaces_regex() -> re.Pattern:
        return re.compile(r'[\t\x0b\x0c\r ]+|^\s*\n', re.MULTILINE)

    @staticmethod
    def remove_whitespaces(source: str) -> str:
        pattern = re.sub(Normalizer.whitespaces_regex(), '', source)
        return pattern.strip()
