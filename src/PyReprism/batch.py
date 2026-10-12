"""Batch/directory processing: analyze or transform whole source trees.

Discovery walks directories, skips common junk folders, and keeps only files
whose extension maps to a supported language. :func:`analyze` returns aggregate
metrics (per file, per language, and totals) exportable as JSON or CSV;
:func:`transform` applies a text transformation across a tree, optionally writing
a mirrored output directory.
"""
import csv
import fnmatch
import io
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from .metrics import CodeStats

PathLike = Union[str, os.PathLike]

_SKIP_DIRS = {
    '.git', '.hg', '.svn', '__pycache__', 'node_modules', '.venv', 'venv', 'env',
    'dist', 'build', '.tox', '.mypy_cache', '.pytest_cache', '.idea', '.vscode',
    'htmlcov', '.eggs',
}

_STAT_FIELDS = (
    'lines', 'code_lines', 'comment_lines', 'blank_lines', 'characters',
    'comment_tokens', 'string_tokens', 'number_tokens', 'keyword_tokens',
    'identifier_tokens', 'operator_tokens',
)


def _zero_stats() -> Dict[str, int]:
    data = {k: 0 for k in _STAT_FIELDS}
    data['files'] = 0
    return data


def _accept(path: Path, include: Optional[Sequence[str]], exclude: Optional[Sequence[str]]) -> bool:
    name, full = path.name, str(path)
    if include and not any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(full, g) for g in include):
        return False
    if exclude and any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(full, g) for g in exclude):
        return False
    return True


def _walk(root: Path, recursive: bool) -> Iterator[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS and not d.startswith('.')]
        for name in sorted(files):
            yield Path(current) / name
        if not recursive:
            dirs[:] = []


def iter_source_files(paths: Union[PathLike, Sequence[PathLike]], *, recursive: bool = True,
                      include: Optional[Sequence[str]] = None,
                      exclude: Optional[Sequence[str]] = None) -> Iterator[Tuple[Path, Path, type]]:
    """Yield ``(base, path, language_cls)`` for every supported source file.

    ``base`` is the top-level input the file was discovered under (used to mirror
    directory structure). Files with an unrecognized extension are skipped.
    """
    from . import detect_language

    if isinstance(paths, (str, os.PathLike)):
        paths = [paths]
    for raw in paths:
        base = Path(raw)
        if base.is_dir():
            candidates = _walk(base, recursive)
        elif base.is_file():
            candidates = [base]
        else:
            continue
        for path in candidates:
            if not _accept(path, include, exclude):
                continue
            cls = detect_language(filename=str(path))
            if cls is not None:
                yield base, path, cls


@dataclass
class FileReport:
    """Metrics for one processed file (``stats`` is ``None`` on error)."""

    path: str
    language: str
    stats: Optional[CodeStats] = None
    error: Optional[str] = None


@dataclass
class BatchReport:
    """Aggregate report over a set of files."""

    files: List[FileReport] = field(default_factory=list)

    @property
    def ok(self) -> List[FileReport]:
        return [f for f in self.files if f.stats is not None]

    @property
    def errors(self) -> List[FileReport]:
        return [f for f in self.files if f.stats is None]

    def totals(self) -> Dict[str, int]:
        total = _zero_stats()
        for report in self.ok:
            total['files'] += 1
            for key in _STAT_FIELDS:
                total[key] += getattr(report.stats, key)
        return total

    def by_language(self) -> Dict[str, Dict[str, int]]:
        out: Dict[str, Dict[str, int]] = {}
        for report in self.ok:
            agg = out.setdefault(report.language, _zero_stats())
            agg['files'] += 1
            for key in _STAT_FIELDS:
                agg[key] += getattr(report.stats, key)
        return dict(sorted(out.items()))

    def to_dict(self) -> dict:
        return {
            'files': [
                {'path': f.path, 'language': f.language, 'error': f.error,
                 **(f.stats.as_dict() if f.stats else {})}
                for f in self.files
            ],
            'by_language': self.by_language(),
            'totals': self.totals(),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_csv(self) -> str:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['path', 'language', *_STAT_FIELDS])
        for report in self.files:
            if report.stats is not None:
                writer.writerow([report.path, report.language,
                                 *[getattr(report.stats, k) for k in _STAT_FIELDS]])
        return buffer.getvalue()


def _language_in_worker(name: str, path: str):
    from . import detect_language
    from ._parallel import language
    return language(name) or detect_language(filename=path)


def _analyze_one(item) -> FileReport:
    path, name, engine = item
    try:
        text = Path(path).read_text(encoding='utf-8', errors='replace')
        cls = _language_in_worker(name, path)
        if engine in (None, 'regex'):
            stats = cls.stats(text)
        else:
            from . import _tokenops
            from .engines import get_engine
            stats = _tokenops.stats(get_engine(engine).tokenize(text, cls), text)
        return FileReport(path, name, stats)
    except Exception as exc:  # pragma: no cover - defensive I/O guard
        return FileReport(path, name, None, str(exc))


def analyze(paths: Union[PathLike, Sequence[PathLike]], *, engine: str = 'regex',
            recursive: bool = True, include: Optional[Sequence[str]] = None,
            exclude: Optional[Sequence[str]] = None, jobs: Optional[int] = 1) -> BatchReport:
    """Walk ``paths`` and compute :class:`CodeStats` for every supported file.

    ``jobs`` sets the number of worker processes (``0`` or ``None``: one per
    CPU); the report is the same for any value.
    """
    from ._parallel import pmap
    items = [(str(path), cls.__name__, engine)
             for _base, path, cls in iter_source_files(paths, recursive=recursive,
                                                       include=include, exclude=exclude)]
    return BatchReport(pmap(_analyze_one, items, jobs))


def _apply_one(item):
    fn, path, name = item
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    return fn(text, _language_in_worker(name, path))


def map_files(paths: Union[PathLike, Sequence[PathLike]], fn: Callable[[str, type], object], *,
              recursive: bool = True, include: Optional[Sequence[str]] = None,
              exclude: Optional[Sequence[str]] = None,
              jobs: Optional[int] = 1) -> List[Tuple[str, type, object]]:
    """Apply ``fn(text, language_cls)`` to every discovered file.

    Returns ``(path, language_cls, result)`` in discovery order. With ``jobs``
    other than 1, files are processed in parallel, and ``fn`` and its results
    must be picklable (e.g. a module-level function returning plain data).
    """
    from ._parallel import pmap
    found = [(path, cls) for _base, path, cls in
             iter_source_files(paths, recursive=recursive, include=include, exclude=exclude)]
    results = pmap(_apply_one, [(fn, str(p), c.__name__) for p, c in found], jobs)
    return [(str(p), c, r) for (p, c), r in zip(found, results)]


def _destination(base: Path, path: Path, output: Path) -> Path:
    if base.is_dir():
        return output / path.relative_to(base)
    return output / path.name


def transform(paths: Union[PathLike, Sequence[PathLike]],
              transformer: Callable[[str, type], str], *,
              output: Optional[PathLike] = None, in_place: bool = False,
              recursive: bool = True, include: Optional[Sequence[str]] = None,
              exclude: Optional[Sequence[str]] = None,
              jobs: Optional[int] = 1) -> List[Tuple[str, str]]:
    """Apply ``transformer(text, language_cls)`` to every discovered file.

    With ``output`` the tree is mirrored under that directory; with ``in_place``
    files are rewritten. Returns ``(path, status)`` pairs. With ``jobs`` other
    than 1, transformations run in parallel and ``transformer`` must be
    picklable (e.g. a module-level function).
    """
    from ._parallel import pmap
    out_root = Path(output) if output else None
    found = list(iter_source_files(paths, recursive=recursive,
                                   include=include, exclude=exclude))
    texts = pmap(_apply_one, [(transformer, str(p), c.__name__) for _b, p, c in found], jobs)
    results: List[Tuple[str, str]] = []
    for (base, path, _cls), transformed in zip(found, texts):
        if out_root is not None:
            dest = _destination(base, path, out_root)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(transformed, encoding='utf-8')
            results.append((str(path), str(dest)))
        elif in_place:
            path.write_text(transformed, encoding='utf-8')
            results.append((str(path), 'in-place'))
        else:
            results.append((str(path), transformed))
    return results
