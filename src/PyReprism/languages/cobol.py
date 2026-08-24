"""COBOL: a dedicated, column-sensitive comment scanner.

COBOL comments do not fit any regex family, so this is hand-written on top of
:class:`~PyReprism.languages._scanners.ScannedLanguage`:

* **Fixed format:** a ``*`` (or ``/`` for a page eject) in the *indicator area*,
  column 7 (0-based index 6), marks the entire line as a comment.
* **Free format (COBOL 2002+):** ``*>`` begins an inline comment that runs to the
  end of the line; ``'...'`` / ``"..."`` string literals are skipped so a ``*>``
  inside a string is not treated as a comment.
"""
from typing import List, Optional, Tuple

from ._scanners import ScannedLanguage
from .registry import LanguageRegistry

_INDICATOR_COL = 6  # column 7, 0-based


def _inline_comment_start(text: str) -> Optional[int]:
    """Index of a free-format ``*>`` comment on ``text`` (a single line without its
    newline), skipping string literals, or ``None``."""
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in '"\'':
            quote = ch
            i += 1
            while i < n and text[i] != quote:
                i += 1
            i += 1  # consume the closing quote (or run off the end)
            continue
        if ch == '*' and i + 1 < n and text[i + 1] == '>':
            return i
        i += 1
    return None


@LanguageRegistry.register
class Cobol(ScannedLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return '.cob'

    @classmethod
    def keywords(cls) -> list:
        return ('IDENTIFICATION|DIVISION|PROGRAM-ID|ENVIRONMENT|CONFIGURATION|'
                'DATA|WORKING-STORAGE|LINKAGE|PROCEDURE|SECTION|PARAGRAPH|PIC|'
                'PICTURE|VALUE|OCCURS|REDEFINES|MOVE|TO|FROM|ADD|SUBTRACT|'
                'MULTIPLY|DIVIDE|COMPUTE|IF|ELSE|END-IF|EVALUATE|WHEN|PERFORM|'
                'UNTIL|VARYING|CALL|USING|DISPLAY|ACCEPT|OPEN|CLOSE|READ|WRITE|'
                'STOP|RUN|GOBACK|EXIT|GO|INITIALIZE|STRING|UNSTRING|INSPECT').split('|')

    @classmethod
    def _comment_spans(cls, source: str) -> List[Tuple[int, int]]:
        spans: List[Tuple[int, int]] = []
        pos = 0
        for line in source.splitlines(keepends=True):
            content = line.rstrip('\n\r')
            content_end = pos + len(content)
            if len(content) > _INDICATOR_COL and content[_INDICATOR_COL] in '*/':
                # Whole line is a comment (leave the newline as code -> blank line).
                spans.append((pos, content_end))
            else:
                idx = _inline_comment_start(content)
                if idx is not None:
                    spans.append((pos + idx, content_end))
            pos += len(line)
        return spans
