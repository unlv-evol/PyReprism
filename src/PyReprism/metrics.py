"""Code metrics produced by :meth:`BaseLanguage.stats`."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CodeStats:
    """Line- and token-level metrics for a source string.

    Line counts are mutually exclusive: ``lines == code_lines + comment_lines +
    blank_lines``. A line with both code and a trailing comment counts as a code
    line.
    """

    lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    characters: int
    comment_tokens: int
    string_tokens: int
    number_tokens: int
    keyword_tokens: int
    identifier_tokens: int
    operator_tokens: int

    @property
    def comment_to_code_ratio(self) -> float:
        """Comment lines divided by code lines (0.0 when there is no code)."""
        return self.comment_lines / self.code_lines if self.code_lines else 0.0

    @property
    def comment_density(self) -> float:
        """Fraction of non-blank lines that are comment-only."""
        non_blank = self.code_lines + self.comment_lines
        return self.comment_lines / non_blank if non_blank else 0.0

    def as_dict(self) -> dict:
        data = asdict(self)
        data['comment_to_code_ratio'] = round(self.comment_to_code_ratio, 4)
        data['comment_density'] = round(self.comment_density, 4)
        return data
