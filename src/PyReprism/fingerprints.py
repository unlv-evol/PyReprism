"""Code fingerprinting and similarity for clone / plagiarism detection.

Uses **winnowing** (Schleimer, Wilkerson & Aiken) over k-grams of a *normalized*
token stream, so matches are robust to renaming and literal changes (Type-2
clones). Hashes are deterministic (CRC32) so fingerprints are stable and
persistable across runs.
"""
import zlib
from collections import defaultdict
from typing import Dict, List, Sequence, Set, Tuple

from .ngrams import ngrams_of
from .tokens import TokenType

_SKIP = {TokenType.WHITESPACE, TokenType.COMMENT}


def normalized_tokens(source: str, lang, *, normalize: bool = True,
                      types: bool = False) -> List[str]:
    """Reduce ``source`` to a token sequence for fingerprinting.

    With ``types`` the token kind is emitted (fully structural). With
    ``normalize`` (default) identifiers/numbers/strings collapse to ``ID``/
    ``NUM``/``STR`` while keywords, operators and punctuation stay literal — so
    renaming variables or changing literals does not change the fingerprint.
    """
    from . import get_language
    cls = lang if isinstance(lang, type) else get_language(lang)
    placeholders = {TokenType.IDENTIFIER: 'ID', TokenType.NUMBER: 'NUM', TokenType.STRING: 'STR'}
    out = []
    for tok in cls.tokenize(source):
        if tok.type in _SKIP:
            continue
        if types:
            out.append(tok.type.value)
        elif normalize and tok.type in placeholders:
            out.append(placeholders[tok.type])
        else:
            out.append(tok.value)
    return out


def _winnow(hashes: Sequence[int], w: int) -> Set[int]:
    """Return the winnowing fingerprint set (selected minimum hashes)."""
    if not hashes:
        return set()
    if len(hashes) < w:
        return {min(hashes)}
    fingerprints: Set[int] = set()
    last = -1
    for i in range(len(hashes) - w + 1):
        window = hashes[i:i + w]
        local_min = min(window)
        # rightmost occurrence of the minimum in the window (per the paper)
        j = i + max(idx for idx, v in enumerate(window) if v == local_min)
        if j != last:
            fingerprints.add(hashes[j])
            last = j
    return fingerprints


def fingerprint(source: str, lang, *, k: int = 5, w: int = 4,
                normalize: bool = True, types: bool = False) -> Set[int]:
    """Return the winnowing fingerprint (set of hashes) of ``source``.

    ``k`` is the k-gram (shingle) size, ``w`` the winnowing window.
    """
    seq = normalized_tokens(source, lang, normalize=normalize, types=types)
    if not seq:
        return set()
    grams = ngrams_of(seq, k) if len(seq) >= k else [tuple(seq)]
    hashes = [zlib.crc32(' '.join(g).encode('utf-8')) for g in grams]
    return _winnow(hashes, w)


def jaccard(a: Set[int], b: Set[int]) -> float:
    """Jaccard similarity of two fingerprint sets, in ``[0, 1]``."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similarity(a: str, b: str, lang, **options) -> float:
    """Similarity (Jaccard of fingerprints) between two sources, in ``[0, 1]``."""
    return jaccard(fingerprint(a, lang, **options), fingerprint(b, lang, **options))


def containment(a: str, b: str, lang, **options) -> float:
    """Fraction of ``a``'s fingerprints also present in ``b`` (asymmetric)."""
    fa = fingerprint(a, lang, **options)
    if not fa:
        return 0.0
    return len(fa & fingerprint(b, lang, **options)) / len(fa)


class FingerprintIndex:
    """An inverted index of fingerprints for many-to-many clone detection."""

    def __init__(self, *, k: int = 5, w: int = 4, normalize: bool = True, types: bool = False):
        self.options = dict(k=k, w=w, normalize=normalize, types=types)
        self.prints: Dict[str, Set[int]] = {}
        self._inverted: Dict[int, Set[str]] = defaultdict(set)

    def add(self, name: str, source: str, lang) -> Set[int]:
        fp = fingerprint(source, lang, **self.options)
        self.prints[name] = fp
        for h in fp:
            self._inverted[h].add(name)
        return fp

    def add_paths(self, paths, *, recursive: bool = True, include=None, exclude=None) -> None:
        """Fingerprint every supported file under ``paths``."""
        from .batch import iter_source_files
        for _base, path, cls in iter_source_files(paths, recursive=recursive,
                                                  include=include, exclude=exclude):
            try:
                self.add(str(path), path.read_text(encoding='utf-8', errors='replace'), cls)
            except Exception:  # pragma: no cover - defensive I/O guard
                continue

    def matches(self, name: str, threshold: float = 0.0) -> List[Tuple[str, float]]:
        """Return ``(other, score)`` for entries similar to ``name``, best first."""
        target = self.prints[name]
        candidates: Set[str] = set()
        for h in target:
            candidates |= self._inverted[h]
        candidates.discard(name)
        scored = [(other, jaccard(target, self.prints[other])) for other in candidates]
        scored = [pair for pair in scored if pair[1] >= threshold]
        return sorted(scored, key=lambda pair: -pair[1])

    def similar_pairs(self, threshold: float = 0.6) -> List[Tuple[str, str, float]]:
        """Return unique ``(a, b, score)`` pairs at or above ``threshold``."""
        seen: Set[Tuple[str, str]] = set()
        pairs: List[Tuple[str, str, float]] = []
        for name in self.prints:
            for other, score in self.matches(name, threshold):
                key = tuple(sorted((name, other)))
                if key in seen:
                    continue
                seen.add(key)
                pairs.append((key[0], key[1], score))
        return sorted(pairs, key=lambda item: -item[2])
