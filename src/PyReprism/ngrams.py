"""Token n-gram analysis and an n-gram language model for code "naturalness".

Built on :meth:`~PyReprism.languages.base.BaseLanguage.tokenize`. Supports value
n-grams (over token text) and *type* n-grams (over token kinds — structural and
AST-free). :class:`NgramModel` estimates a smoothed n-gram distribution over a
corpus so a file's cross-entropy / perplexity can be measured, following Hindle
et al., "On the Naturalness of Software".
"""
import json
import math
from collections import Counter
from typing import Iterable, List, Optional, Sequence, Tuple

from .tokens import TokenType

START, END = '<s>', '</s>'
_SKIP = {TokenType.WHITESPACE}


def token_sequence(source: str, lang, *, types: bool = False,
                   include_comments: bool = False) -> List[str]:
    """Reduce ``source`` to a flat list of token strings.

    With ``types`` the token *kind* is emitted instead of its text (structural
    n-grams). Whitespace is always skipped; comments are skipped unless
    ``include_comments``.
    """
    from . import get_language
    cls = get_language(lang) if not isinstance(lang, type) else lang
    skip = set(_SKIP)
    if not include_comments:
        skip.add(TokenType.COMMENT)
    out = []
    for tok in cls.tokenize(source):
        if tok.type in skip:
            continue
        out.append(tok.type.value if types else tok.value)
    return out


def ngrams(source: str, lang, n: int = 3, *, types: bool = False,
           include_comments: bool = False, pad: bool = False) -> List[Tuple[str, ...]]:
    """Return the list of token ``n``-grams in ``source``."""
    seq = token_sequence(source, lang, types=types, include_comments=include_comments)
    return ngrams_of(seq, n, pad=pad)


def ngrams_of(seq: Sequence[str], n: int, *, pad: bool = False) -> List[Tuple[str, ...]]:
    """Return the ``n``-grams of a token sequence."""
    if n < 1:
        raise ValueError("n must be >= 1")
    if pad:
        seq = [START] * (n - 1) + list(seq) + [END]
    return [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]


def ngram_counts(source: str, lang, n: int = 3, **kwargs) -> Counter:
    """Return a :class:`collections.Counter` of ``n``-grams in ``source``."""
    return Counter(ngrams(source, lang, n, **kwargs))


class NgramModel:
    """A smoothed n-gram language model over token sequences.

    Train with :meth:`fit`/:meth:`update` (sequences of token strings), then score
    a sequence's :meth:`cross_entropy` or :meth:`perplexity`. Uses add-k
    (Laplace) smoothing with an implicit unknown-token slot.
    """

    def __init__(self, n: int = 3, k: float = 1.0, types: bool = False):
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.k = k
        self.types = types
        self.ngram_counts: Counter = Counter()
        self.context_counts: Counter = Counter()
        self.vocab: set = set()

    # ---------------------------------------------------------------- training
    def update(self, seq: Sequence[str]) -> "NgramModel":
        padded = [START] * (self.n - 1) + list(seq) + [END]
        for i in range(self.n - 1, len(padded)):
            context = tuple(padded[i - (self.n - 1):i])
            token = padded[i]
            self.ngram_counts[context + (token,)] += 1
            self.context_counts[context] += 1
            self.vocab.add(token)
        return self

    def fit(self, sequences: Iterable[Sequence[str]]) -> "NgramModel":
        for seq in sequences:
            self.update(seq)
        return self

    # ----------------------------------------------------------------- scoring
    @property
    def vocab_size(self) -> int:
        return len(self.vocab) + 1  # + 1 for unseen (<unk>) tokens

    def _logprob(self, context: Tuple[str, ...], token: str) -> float:
        num = self.ngram_counts.get(context + (token,), 0) + self.k
        den = self.context_counts.get(context, 0) + self.k * self.vocab_size
        return math.log2(num / den)

    def logprob(self, seq: Sequence[str]) -> float:
        """Total log2-probability of ``seq`` under the model."""
        padded = [START] * (self.n - 1) + list(seq) + [END]
        total = 0.0
        for i in range(self.n - 1, len(padded)):
            context = tuple(padded[i - (self.n - 1):i])
            total += self._logprob(context, padded[i])
        return total

    def cross_entropy(self, seq: Sequence[str]) -> float:
        """Average bits per token (lower = more predictable / "natural")."""
        count = len(seq) + 1  # predicted tokens include the END marker
        if count == 0:
            return 0.0
        return -self.logprob(seq) / count

    def perplexity(self, seq: Sequence[str]) -> float:
        """``2 ** cross_entropy`` — lower means more natural."""
        return 2 ** self.cross_entropy(seq)

    # ------------------------------------------------------------- persistence
    def to_dict(self) -> dict:
        return {
            'n': self.n, 'k': self.k, 'types': self.types,
            'vocab': sorted(self.vocab),
            'ngrams': [[list(g), c] for g, c in self.ngram_counts.items()],
            'contexts': [[list(g), c] for g, c in self.context_counts.items()],
        }

    def save(self, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(self.to_dict(), handle)

    @classmethod
    def from_dict(cls, data: dict) -> "NgramModel":
        model = cls(n=data['n'], k=data.get('k', 1.0), types=data.get('types', False))
        model.vocab = set(data.get('vocab', []))
        model.ngram_counts = Counter({tuple(g): c for g, c in data.get('ngrams', [])})
        model.context_counts = Counter({tuple(g): c for g, c in data.get('contexts', [])})
        return model

    @classmethod
    def load(cls, path: str) -> "NgramModel":
        with open(path, 'r', encoding='utf-8') as handle:
            return cls.from_dict(json.load(handle))


def train(paths, *, n: int = 3, types: bool = False, include_comments: bool = False,
          recursive: bool = True, include=None, exclude=None,
          lang: Optional[str] = None) -> NgramModel:
    """Train an :class:`NgramModel` over a corpus (files or directories)."""
    from .batch import iter_source_files

    model = NgramModel(n=n, types=types)
    for _base, path, cls in iter_source_files(paths, recursive=recursive,
                                              include=include, exclude=exclude):
        language = lang or cls
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
            model.update(token_sequence(text, language, types=types,
                                        include_comments=include_comments))
        except Exception:  # pragma: no cover - defensive I/O guard
            continue
    return model
