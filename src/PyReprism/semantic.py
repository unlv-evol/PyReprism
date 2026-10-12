"""Semantic tier: neural code embeddings for Type-4 (semantically equivalent,
syntactically different) clone detection.

This is the highest-fidelity rung of PyReprism's analysis ladder and the only one
that is *not* lexical: token fingerprints (see :mod:`PyReprism.fingerprints`)
detect Type-1/2/3 clones but cannot detect Type-4 clones, which share little
surface form. Here we embed code with a code-search transformer and rank by cosine
similarity, mirroring the :class:`~PyReprism.fingerprints.FingerprintIndex` API.

Everything here is optional: it requires ``pip install pyreprism[semantic]``
(``transformers`` + ``torch``). Import succeeds without them, but calling into the
tier raises a clear error, and :func:`available` reports readiness---so the
zero-dependency lexical core is never affected.
"""
from functools import lru_cache
from typing import List, Sequence, Tuple

# A DistilRoBERTa fine-tuned for code search (CodeSearchNet): produces embeddings
# whose cosine similarity separates semantic clones from unrelated code.
DEFAULT_MODEL = "flax-sentence-embeddings/st-codesearch-distilroberta-base"


def available() -> bool:
    """True if the optional embedding backend can be imported."""
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
        return True
    except ImportError:
        return False


def _require():
    if not available():
        raise ImportError(
            "the semantic tier requires transformers+torch; install with "
            "`pip install pyreprism[semantic]`."
        )


@lru_cache(maxsize=4)
def _load(model_name: str):
    _require()
    import torch
    from transformers import AutoModel, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModel.from_pretrained(model_name)
    mdl.eval()
    return tok, mdl, torch


def embed(codes: Sequence[str], model_name: str = DEFAULT_MODEL,
          batch_size: int = 16, max_length: int = 256):
    """Return L2-normalized mean-pooled embeddings for ``codes`` as an array
    of shape ``(len(codes), dim)``."""
    import numpy as np
    tok, mdl, torch = _load(model_name)
    vecs = []
    codes = list(codes)
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i + batch_size]
        enc = tok(batch, return_tensors="pt", truncation=True,
                  max_length=max_length, padding=True)
        with torch.no_grad():
            hidden = mdl(**enc).last_hidden_state          # (B, T, H)
        mask = enc["attention_mask"].unsqueeze(-1).float()
        pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
        pooled = torch.nn.functional.normalize(pooled, dim=1)
        vecs.append(pooled.cpu().numpy())
    return np.vstack(vecs) if vecs else np.zeros((0, 0))


def similarity(code_a: str, code_b: str, model_name: str = DEFAULT_MODEL) -> float:
    """Cosine similarity of two code snippets in embedding space (in ``[-1, 1]``)."""
    v = embed([code_a, code_b], model_name=model_name)
    return float(v[0] @ v[1])


class EmbeddingIndex:
    """A many-to-many semantic clone index, parallel to
    :class:`~PyReprism.fingerprints.FingerprintIndex` but embedding-based.

    Add named documents, then query by similarity or list all near-duplicate
    pairs above a cosine threshold.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self._names: List[str] = []
        self._codes: List[str] = []
        self._vecs = None  # lazily (re)computed

    def add(self, name: str, code: str) -> None:
        self._names.append(name)
        self._codes.append(code)
        self._vecs = None

    def add_paths(self, root: str, encoding: str = "utf-8") -> int:
        """Add every file under ``root`` (best effort); returns the count added."""
        import os
        n = 0
        for base, _dirs, files in os.walk(root):
            for f in files:
                p = os.path.join(base, f)
                try:
                    with open(p, "r", encoding=encoding, errors="replace") as fh:
                        self.add(p, fh.read())
                    n += 1
                except OSError:
                    continue
        return n

    def _ensure(self):
        import numpy as np
        if self._vecs is None:
            self._vecs = (embed(self._codes, model_name=self.model_name)
                          if self._codes else np.zeros((0, 0)))
        return self._vecs

    def query(self, code: str, k: int = 5) -> List[Tuple[str, float]]:
        """Return the ``k`` most semantically similar indexed documents."""
        vecs = self._ensure()
        if len(self._names) == 0:
            return []
        q = embed([code], model_name=self.model_name)[0]
        sims = vecs @ q
        order = sims.argsort()[::-1][:k]
        return [(self._names[i], float(sims[i])) for i in order]

    def similar_pairs(self, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
        """All document pairs with cosine similarity ``>= threshold``, descending."""
        vecs = self._ensure()
        out = []
        n = len(self._names)
        for i in range(n):
            for j in range(i + 1, n):
                s = float(vecs[i] @ vecs[j])
                if s >= threshold:
                    out.append((self._names[i], self._names[j], s))
        out.sort(key=lambda t: t[2], reverse=True)
        return out


def clone_type_note() -> str:
    """One-line description of where this tier sits on the analysis ladder."""
    return ("semantic (embedding) tier: detects Type-4 clones that lexical "
            "fingerprints miss; optional, requires pyreprism[semantic].")
