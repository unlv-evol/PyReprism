"""Located clone detection with a unified, multi-tier report.

This complements :mod:`PyReprism.fingerprints` (which returns a file-level
*similarity score*) with jscpd-style **located fragments**: it reports which line
ranges are duplicated between two files, found by a Rabin-Karp scan over the
normalized token stream. Crucially, the same report model carries clones from all
three rungs of the fidelity ladder, each tagged with a ``kind``:

* ``exact``    -- Type-1/2 located fragments (Rabin-Karp; rename-invariant when
                  normalized). These have real line ranges in both files.
* ``near``     -- Type-3 file-level near-duplicates (winnowing fingerprints).
* ``semantic`` -- Type-4 clones (code embeddings), at function granularity when
                  the syntactic tier is available, else file level.

Every clone flows through the same :mod:`PyReprism.reporters` (json / sarif /
markdown / console), so a CI pipeline can surface lexical *and* semantic
duplication uniformly, with a distinct rule id per kind.
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .tokens import TokenType

_SKIP = {TokenType.WHITESPACE, TokenType.COMMENT}
_PLACEHOLDER = {TokenType.IDENTIFIER: 'ID', TokenType.NUMBER: 'NUM',
                TokenType.STRING: 'STR'}

DEFAULT_MIN_TOKENS = 50
DEFAULT_MIN_LINES = 5


@dataclass
class Fragment:
    """A located region of code: a line range within one file."""
    path: str
    start_line: int
    end_line: int
    start_token: int = 0
    end_token: int = 0

    @property
    def lines(self) -> int:
        return self.end_line - self.start_line + 1


@dataclass
class Clone:
    """A duplicated pair. ``kind`` is ``exact`` / ``near`` / ``semantic``."""
    kind: str
    a: Fragment
    b: Fragment
    score: float
    tokens: int = 0

    def as_dict(self) -> dict:
        return {
            'kind': self.kind, 'score': round(self.score, 4), 'tokens': self.tokens,
            'a': {'path': self.a.path, 'startLine': self.a.start_line,
                  'endLine': self.a.end_line},
            'b': {'path': self.b.path, 'startLine': self.b.start_line,
                  'endLine': self.b.end_line},
        }


@dataclass
class CloneReport:
    clones: List[Clone] = field(default_factory=list)
    files: int = 0
    total_lines: int = 0
    duplicated_lines: int = 0

    @property
    def duplication_pct(self) -> float:
        return round(100.0 * self.duplicated_lines / self.total_lines, 2) \
            if self.total_lines else 0.0

    def by_kind(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for c in self.clones:
            out[c.kind] = out.get(c.kind, 0) + 1
        return out

    def summary(self) -> dict:
        return {'files': self.files, 'clones': len(self.clones),
                'by_kind': self.by_kind(), 'total_lines': self.total_lines,
                'duplicated_lines': self.duplicated_lines,
                'duplication_pct': self.duplication_pct}


# --------------------------------------------------------------- tokenization
def _tokens_with_lines(source: str, cls, normalize: bool = True) -> List[Tuple[str, int]]:
    """Normalized ``(value, line)`` tokens, dropping whitespace/comments."""
    out = []
    for tok in cls.tokenize(source):
        if tok.type in _SKIP:
            continue
        if normalize and tok.type in _PLACEHOLDER:
            out.append((_PLACEHOLDER[tok.type], tok.line))
        else:
            out.append((tok.value, tok.line))
    return out


def _tokens_in_worker(item) -> List[Tuple[str, int]]:
    from . import detect_language
    from ._parallel import language
    src, name, path, normalize = item
    cls = language(name) or detect_language(filename=path)
    return _tokens_with_lines(src, cls, normalize)


def _line_count(source: str) -> int:
    return source.count('\n') + 1


# ------------------------------------------------------ Rabin-Karp exact clones
def find_exact_clones(tokens: Dict[str, List[Tuple[str, int]]], *,
                      min_tokens: int = DEFAULT_MIN_TOKENS,
                      min_lines: int = DEFAULT_MIN_LINES) -> List[Clone]:
    """Locate maximal duplicated token runs across files (Type-1/2 fragments).

    ``tokens`` maps a path to its ``(value, line)`` token list. A window of
    ``min_tokens`` seeds a match, which is greedily extended; fragments shorter
    than ``min_lines`` lines are dropped.
    """
    from collections import defaultdict
    seqs = {name: [v for v, _ln in toks] for name, toks in tokens.items()}
    L = max(1, min_tokens)
    index: Dict[int, List[Tuple[str, int]]] = defaultdict(list)
    for name, seq in seqs.items():
        for i in range(len(seq) - L + 1):
            index[hash(tuple(seq[i:i + L]))].append((name, i))

    covered: Dict[str, set] = defaultdict(set)
    clones: List[Clone] = []
    for occ in index.values():
        if len(occ) < 2:
            continue
        for a in range(len(occ)):
            na, ia = occ[a]
            for b in range(a + 1, len(occ)):
                nb, ib = occ[b]
                if na == nb and abs(ia - ib) < L:
                    continue
                if ia in covered[na] and ib in covered[nb]:
                    continue
                if seqs[na][ia:ia + L] != seqs[nb][ib:ib + L]:
                    continue  # hash collision
                la, lb = len(seqs[na]), len(seqs[nb])
                ext = L
                while (ia + ext < la and ib + ext < lb
                       and seqs[na][ia + ext] == seqs[nb][ib + ext]):
                    ext += 1
                fa = _fragment(na, tokens[na], ia, ia + ext)
                fb = _fragment(nb, tokens[nb], ib, ib + ext)
                if min(fa.lines, fb.lines) < min_lines:
                    continue
                clones.append(Clone('exact', fa, fb, 1.0, tokens=ext))
                for p in range(ia, ia + ext):
                    covered[na].add(p)
                for p in range(ib, ib + ext):
                    covered[nb].add(p)
    clones.sort(key=lambda c: c.tokens, reverse=True)
    return clones


def _fragment(name: str, toks: List[Tuple[str, int]], start: int, end: int) -> Fragment:
    return Fragment(name, toks[start][1], toks[end - 1][1], start, end)


def _duplicated_line_count(clones: List[Clone], only_kinds=('exact',)) -> Dict[str, set]:
    """Union of covered line numbers per file (from located clones)."""
    from collections import defaultdict
    per_file: Dict[str, set] = defaultdict(set)
    for c in clones:
        if c.kind not in only_kinds:
            continue
        for frag in (c.a, c.b):
            per_file[frag.path].update(range(frag.start_line, frag.end_line + 1))
    return per_file


# ------------------------------------------------------------------ gathering
def _gather(paths, lang: Optional[str]) -> Dict[str, Tuple[str, object]]:
    """Return ``{path: (source, language_class)}`` for files under ``paths``."""
    from . import detect_language, get_language
    from .batch import iter_source_files
    files: Dict[str, Tuple[str, object]] = {}

    def add_file(p: str):
        try:
            with open(p, 'r', encoding='utf-8', errors='replace') as fh:
                src = fh.read()
        except OSError:
            return
        cls = get_language(lang) if lang else detect_language(filename=p)
        if cls is not None:
            files[p] = (src, cls)

    for path in paths:
        if os.path.isdir(path):
            for _base, p, cls in iter_source_files(path):
                try:
                    src = p.read_text(encoding='utf-8', errors='replace')
                except OSError:
                    continue
                files[str(p)] = (src, get_language(lang) if lang else cls)
        else:
            add_file(path)
    return files


# --------------------------------------------------------- semantic (Type-4)
def _semantic_clones(files: Dict[str, Tuple[str, object]], *, threshold: float,
                     functions: bool) -> List[Clone]:
    """Embedding-based Type-4 clones. Function-level when the syntactic tier is
    available (located fragments); otherwise whole-file."""
    from . import semantic
    if not semantic.available():
        return []
    from . import syntactic

    units: List[Tuple[str, int, int, str]] = []  # (path, start_line, end_line, code)
    use_functions = functions and syntactic.available()
    for path, (src, cls) in files.items():
        ts = syntactic._ts_name(cls.__name__.lower()) if use_functions else None
        added = False
        if ts:
            try:
                for fn in syntactic.functions(src, ts):
                    code = src.encode('utf-8', 'replace')[fn.start_byte:fn.end_byte]
                    code = code.decode('utf-8', 'replace')
                    end_line = fn.start_line + code.count('\n')
                    units.append((path, fn.start_line, end_line, code))
                    added = True
            except Exception:
                added = False
        if not added:
            units.append((path, 1, _line_count(src), src))

    if len(units) < 2:
        return []
    vecs = semantic.embed([u[3] for u in units])
    clones: List[Clone] = []
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            if units[i][0] == units[j][0]:
                continue  # different files only
            score = float(vecs[i] @ vecs[j])
            if score >= threshold:
                pa, sa, ea, _ = units[i]
                pb, sb, eb, _ = units[j]
                clones.append(Clone('semantic', Fragment(pa, sa, ea),
                                    Fragment(pb, sb, eb), score))
    clones.sort(key=lambda c: c.score, reverse=True)
    return clones


# ------------------------------------------------------------------- detect
def detect(paths, *, lang: Optional[str] = None,
           min_tokens: int = DEFAULT_MIN_TOKENS, min_lines: int = DEFAULT_MIN_LINES,
           normalize: bool = True, near: bool = False, near_threshold: float = 0.8,
           semantic: bool = False, semantic_threshold: float = 0.8,
           semantic_functions: bool = True, jobs: Optional[int] = 1) -> CloneReport:
    """Detect clones under ``paths`` and return a unified :class:`CloneReport`.

    Always locates ``exact`` fragments. ``near`` adds file-level Type-3 pairs
    (winnowing fingerprints); ``semantic`` adds Type-4 pairs (embeddings), at
    function granularity when the syntactic tier is available. ``jobs`` sets
    the number of processes that tokenize files (``0`` or ``None``: one per
    CPU); the report is the same for any value.
    """
    from ._parallel import pmap
    files = _gather(paths if isinstance(paths, (list, tuple)) else [paths], lang)
    items = [(src, cls.__name__, p, normalize) for p, (src, cls) in files.items()]
    tokens = dict(zip(files, pmap(_tokens_in_worker, items, jobs)))

    clones = find_exact_clones(tokens, min_tokens=min_tokens, min_lines=min_lines)

    seen_pairs = {frozenset((c.a.path, c.b.path)) for c in clones}
    if near:
        from .fingerprints import FingerprintIndex
        idx = FingerprintIndex(normalize=normalize)
        for p, (src, cls) in files.items():
            idx.add(p, src, cls)
        for a, b, score in idx.similar_pairs(near_threshold):
            if frozenset((a, b)) in seen_pairs:
                continue
            clones.append(Clone('near', _whole(a, files), _whole(b, files), score))
            seen_pairs.add(frozenset((a, b)))
    if semantic:
        for c in _semantic_clones(files, threshold=semantic_threshold,
                                  functions=semantic_functions):
            if frozenset((c.a.path, c.b.path)) in seen_pairs:
                continue
            clones.append(c)

    total_lines = sum(_line_count(src) for src, _cls in files.values())
    dup = _duplicated_line_count(clones, only_kinds=('exact',))
    duplicated_lines = sum(len(v) for v in dup.values())
    return CloneReport(clones=clones, files=len(files), total_lines=total_lines,
                       duplicated_lines=duplicated_lines)


def _whole(path: str, files: Dict[str, Tuple[str, object]]) -> Fragment:
    src = files[path][0]
    return Fragment(path, 1, _line_count(src))
