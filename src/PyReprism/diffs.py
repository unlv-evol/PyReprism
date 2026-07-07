"""Process unified/``git`` diffs with PyReprism's language-aware operations.

A diff is parsed into files and hunks; each file's path is used to detect its
language, so the added/removed code can be tokenized, normalized, or measured.

Two accuracy modes:

* **Fragment mode** (default) works from the diff text alone. It is self-contained
  but best-effort where a block comment or string spans a hunk boundary.
* **Full-file mode** is used automatically for a :class:`DiffFile` when its
  ``new_source`` / ``old_source`` are set (e.g. from ``git show``); changed lines
  are then classified against the whole file for accuracy.
"""
import csv
import io
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .tokens import TokenType

_HUNK_RE = re.compile(r'^@@+ (?:-\d+(?:,\d+)? )+\+(\d+)(?:,(\d+))? @@+(.*)$')
_HUNK_OLD_RE = re.compile(r'-(\d+)(?:,(\d+))?')


class LineKind(str, Enum):
    CONTEXT = 'context'
    ADDED = 'added'
    REMOVED = 'removed'


@dataclass(frozen=True)
class DiffLine:
    kind: LineKind
    text: str                       # content without the +/-/space prefix
    old_lineno: Optional[int]
    new_lineno: Optional[int]


@dataclass
class Hunk:
    old_start: int
    new_start: int
    section: str = ''
    lines: List[DiffLine] = field(default_factory=list)


@dataclass
class DiffFile:
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    hunks: List[Hunk] = field(default_factory=list)
    is_binary: bool = False
    is_new: bool = False
    is_deleted: bool = False
    is_rename: bool = False
    # Optional whole-file contents for accurate (full-file) classification.
    new_source: Optional[str] = None
    old_source: Optional[str] = None

    @property
    def path(self) -> Optional[str]:
        """The most representative path (new side, falling back to old side)."""
        return self.new_path or self.old_path

    @property
    def language(self):
        """Detected language class for this file, or ``None``."""
        from . import detect_language
        if self.path:
            return detect_language(filename=self.path)
        return None

    # -- reconstruction -----------------------------------------------------
    def _collect(self, kinds) -> List[DiffLine]:
        return [dl for h in self.hunks for dl in h.lines if dl.kind in kinds]

    def added_text(self) -> str:
        """Text of the added (``+``) lines."""
        return '\n'.join(dl.text for dl in self._collect((LineKind.ADDED,)))

    def removed_text(self) -> str:
        """Text of the removed (``-``) lines."""
        return '\n'.join(dl.text for dl in self._collect((LineKind.REMOVED,)))

    def new_text(self) -> str:
        """The new side of the hunks (context + added lines)."""
        return '\n'.join(dl.text for dl in self._collect((LineKind.CONTEXT, LineKind.ADDED)))

    def old_text(self) -> str:
        """The old side of the hunks (context + removed lines)."""
        return '\n'.join(dl.text for dl in self._collect((LineKind.CONTEXT, LineKind.REMOVED)))

    def changed_text(self, side: str = 'added') -> str:
        return self.added_text() if side == 'added' else self.removed_text()

    # -- language-aware analyses -------------------------------------------
    def tokenize(self, side: str = 'added'):
        """Tokenize the changed code on ``side`` (``'added'`` or ``'removed'``)."""
        lang = self.language
        if lang is None:
            return []
        return lang.tokenize(self.changed_text(side))

    def normalize(self, side: str = 'added', **options) -> str:
        """Canonicalize the changed code on ``side`` for ML/clone detection."""
        lang = self.language
        text = self.changed_text(side)
        return lang.normalize(text, **options) if lang is not None else text

    def extract_comments(self, side: str = 'added') -> List[str]:
        lang = self.language
        if lang is None:
            return []
        return lang.extract_comments(self.changed_text(side))


@dataclass
class Diff:
    files: List[DiffFile] = field(default_factory=list)

    def __iter__(self):
        return iter(self.files)

    def __len__(self):
        return len(self.files)


# --------------------------------------------------------------------- parsing
def _clean_path(raw: str) -> Optional[str]:
    path = raw.split('\t', 1)[0].strip()
    if path == '/dev/null':
        return None
    if path.startswith(('a/', 'b/')):
        path = path[2:]
    return path or None


def parse(text: str) -> Diff:
    """Parse unified/``git`` diff ``text`` into a :class:`Diff`."""
    files: List[DiffFile] = []
    current: Optional[DiffFile] = None
    hunk: Optional[Hunk] = None
    rem_old = rem_new = 0
    old_ln = new_ln = 0

    def start_file() -> DiffFile:
        f = DiffFile()
        files.append(f)
        return f

    for line in text.splitlines():
        if line.startswith('diff --git'):
            current = start_file()
            hunk = None
            parts = line.split(' ')
            if len(parts) >= 4:
                current.old_path = _clean_path(parts[-2])
                current.new_path = _clean_path(parts[-1])
            continue
        if line.startswith('--- '):
            if current is None or current.hunks or hunk is not None:
                current = start_file()
            current.old_path = _clean_path(line[4:])
            hunk = None
            continue
        if line.startswith('+++ '):
            if current is None:
                current = start_file()
            current.new_path = _clean_path(line[4:])
            continue
        if current is not None:
            if line.startswith('new file'):
                current.is_new = True
                continue
            if line.startswith('deleted file'):
                current.is_deleted = True
                continue
            if line.startswith('rename from '):
                current.is_rename = True
                current.old_path = _clean_path(line[len('rename from '):])
                continue
            if line.startswith('rename to '):
                current.is_rename = True
                current.new_path = _clean_path(line[len('rename to '):])
                continue
            if line.startswith('Binary files') or line.startswith('GIT binary patch'):
                current.is_binary = True
                continue
            if line.startswith(('index ', 'similarity ', 'copy ', 'old mode', 'new mode',
                                'dissimilarity')):
                continue
        match = _HUNK_RE.match(line)
        if match and current is not None:
            old_match = _HUNK_OLD_RE.search(line)
            old_start = int(old_match.group(1)) if old_match else 0
            old_count = int(old_match.group(2)) if old_match and old_match.group(2) else 1
            new_start = int(match.group(1))
            new_count = int(match.group(2)) if match.group(2) else 1
            hunk = Hunk(old_start=old_start, new_start=new_start, section=match.group(3).strip())
            current.hunks.append(hunk)
            rem_old, rem_new = old_count, new_count
            old_ln, new_ln = old_start, new_start
            continue
        if hunk is not None and (rem_old > 0 or rem_new > 0):
            if line.startswith('\\'):  # "\ No newline at end of file"
                continue
            prefix = line[:1]
            content = line[1:]
            if prefix == '+':
                hunk.lines.append(DiffLine(LineKind.ADDED, content, None, new_ln))
                new_ln += 1
                rem_new -= 1
            elif prefix == '-':
                hunk.lines.append(DiffLine(LineKind.REMOVED, content, old_ln, None))
                old_ln += 1
                rem_old -= 1
            elif prefix == ' ' or line == '':
                hunk.lines.append(DiffLine(LineKind.CONTEXT, content, old_ln, new_ln))
                old_ln += 1
                new_ln += 1
                rem_old -= 1
                rem_new -= 1
            else:
                hunk = None
    return Diff(files)


# ------------------------------------------------------------------- analyses
def _line_classes(source: str, lang) -> Dict[int, str]:
    """Map 1-based line number -> 'code' | 'comment' | 'blank' for ``source``."""
    classes: Dict[int, str] = {}
    total = len(source.splitlines())
    if lang is None:
        for i, line in enumerate(source.splitlines(), 1):
            classes[i] = 'code' if line.strip() else 'blank'
        return classes
    code, comment = set(), set()
    for tok in lang.tokenize(source):
        if tok.type is TokenType.WHITESPACE:
            continue
        span = range(tok.line, tok.line + tok.value.count('\n') + 1)
        (comment if tok.type is TokenType.COMMENT else code).update(span)
    for i in range(1, total + 1):
        if i in code:
            classes[i] = 'code'
        elif i in comment:
            classes[i] = 'comment'
        else:
            classes[i] = 'blank'
    return classes


def _side_counts(file: DiffFile, side: str) -> Dict[str, int]:
    lang = file.language
    kind = LineKind.ADDED if side == 'added' else LineKind.REMOVED
    lines = [dl for h in file.hunks for dl in h.lines if dl.kind is kind]
    source = file.new_source if side == 'added' else file.old_source
    counts = {'code': 0, 'comment': 0, 'blank': 0}

    if source is not None:
        classes = _line_classes(source, lang)
        for dl in lines:
            lineno = dl.new_lineno if side == 'added' else dl.old_lineno
            counts[classes.get(lineno, 'code')] += 1
        return counts

    # Fragment mode: classify the reconstructed blob.
    if not lines:
        return counts
    blob = '\n'.join(dl.text for dl in lines)
    if lang is None:
        nonblank = sum(1 for dl in lines if dl.text.strip())
        counts['code'] = nonblank
        counts['blank'] = len(lines) - nonblank
        return counts
    stats = lang.stats(blob)
    counts['code'] = stats.code_lines
    counts['comment'] = stats.comment_lines
    counts['blank'] = stats.blank_lines
    return counts


@dataclass
class DiffFileStats:
    path: Optional[str]
    language: Optional[str]
    added_code: int = 0
    added_comment: int = 0
    added_blank: int = 0
    removed_code: int = 0
    removed_comment: int = 0
    removed_blank: int = 0
    is_binary: bool = False

    @property
    def added(self) -> int:
        return self.added_code + self.added_comment + self.added_blank

    @property
    def removed(self) -> int:
        return self.removed_code + self.removed_comment + self.removed_blank

    def as_dict(self) -> dict:
        data = {k: getattr(self, k) for k in (
            'path', 'language', 'added_code', 'added_comment', 'added_blank',
            'removed_code', 'removed_comment', 'removed_blank', 'is_binary')}
        data['added'] = self.added
        data['removed'] = self.removed
        return data


_STAT_KEYS = ('added_code', 'added_comment', 'added_blank',
              'removed_code', 'removed_comment', 'removed_blank')


@dataclass
class DiffReport:
    files: List[DiffFileStats] = field(default_factory=list)

    def totals(self) -> Dict[str, int]:
        total = {k: 0 for k in _STAT_KEYS}
        total['files'] = len(self.files)
        for f in self.files:
            for k in _STAT_KEYS:
                total[k] += getattr(f, k)
        total['added'] = sum(getattr(f, 'added') for f in self.files)
        total['removed'] = sum(getattr(f, 'removed') for f in self.files)
        return total

    def to_dict(self) -> dict:
        return {'files': [f.as_dict() for f in self.files], 'totals': self.totals()}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_csv(self) -> str:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['path', 'language', *_STAT_KEYS, 'is_binary'])
        for f in self.files:
            writer.writerow([f.path, f.language, *[getattr(f, k) for k in _STAT_KEYS],
                             f.is_binary])
        return buffer.getvalue()


def diff_stats(diff: Diff) -> DiffReport:
    """Compute per-file added/removed churn split into code / comment / blank."""
    rows = []
    for file in diff.files:
        lang = file.language
        lang_name = lang.__name__ if lang is not None else None
        if file.is_binary:
            rows.append(DiffFileStats(file.path, lang_name, is_binary=True))
            continue
        added = _side_counts(file, 'added')
        removed = _side_counts(file, 'removed')
        rows.append(DiffFileStats(
            file.path, lang_name,
            added_code=added['code'], added_comment=added['comment'], added_blank=added['blank'],
            removed_code=removed['code'], removed_comment=removed['comment'],
            removed_blank=removed['blank']))
    return DiffReport(rows)


def _code_only(lang, text: str) -> str:
    from . import remove_whitespaces
    if lang is None:
        return remove_whitespaces(text)
    return remove_whitespaces(lang.remove_comments(text))


def is_cosmetic_change(file: DiffFile) -> bool:
    """True if the file's change is comments/whitespace only (no code change)."""
    if file.is_binary:
        return False
    lang = file.language
    if file.new_source is not None and file.old_source is not None:
        old, new = file.old_source, file.new_source
    else:
        old, new = file.old_text(), file.new_text()
    if not file.hunks:
        return False
    return _code_only(lang, old) == _code_only(lang, new)


def cosmetic_files(diff: Diff) -> List[DiffFile]:
    """Return the files whose change is comment/whitespace only."""
    return [f for f in diff.files if is_cosmetic_change(f)]
