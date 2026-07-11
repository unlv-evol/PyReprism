"""Code metrics produced by :meth:`BaseLanguage.stats` and friends."""
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Halstead:
    """`Halstead complexity measures <https://en.wikipedia.org/wiki/Halstead_complexity_measures>`_.

    Derived from token counts: operators are operator/keyword/punctuation tokens,
    operands are identifier/number/string tokens.
    """

    distinct_operators: int   # n1
    distinct_operands: int    # n2
    total_operators: int      # N1
    total_operands: int       # N2

    @property
    def vocabulary(self) -> int:
        return self.distinct_operators + self.distinct_operands

    @property
    def length(self) -> int:
        return self.total_operators + self.total_operands

    @property
    def volume(self) -> float:
        return self.length * math.log2(self.vocabulary) if self.vocabulary else 0.0

    @property
    def difficulty(self) -> float:
        if not self.distinct_operands:
            return 0.0
        return (self.distinct_operators / 2) * (self.total_operands / self.distinct_operands)

    @property
    def effort(self) -> float:
        return self.difficulty * self.volume

    @property
    def time_seconds(self) -> float:
        """Estimated implementation time (Halstead's ``E / 18``)."""
        return self.effort / 18

    @property
    def bugs(self) -> float:
        """Estimated delivered bugs (``V / 3000``)."""
        return self.volume / 3000

    def as_dict(self) -> dict:
        data = asdict(self)
        data.update(
            vocabulary=self.vocabulary,
            length=self.length,
            volume=round(self.volume, 2),
            difficulty=round(self.difficulty, 2),
            effort=round(self.effort, 2),
            time_seconds=round(self.time_seconds, 2),
            bugs=round(self.bugs, 4),
        )
        return data


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
