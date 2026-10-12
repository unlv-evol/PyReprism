"""Tests for the optional semantic (embedding) tier.

Skipped when transformers/torch are not installed
(``pip install pyreprism[semantic]``). The model is loaded once; kept minimal to
bound test time.
"""
import pytest

from PyReprism import semantic

if not semantic.available():
    pytest.skip("transformers/torch not installed", allow_module_level=True)


def test_embed_shape_and_norm():
    import numpy as np
    v = semantic.embed(["def add(a, b): return a + b", "int x = 0;"])
    assert v.shape[0] == 2 and v.shape[1] > 0
    assert np.allclose(np.linalg.norm(v, axis=1), 1.0, atol=1e-3)  # L2-normalized


def test_similarity_separates_clone_from_unrelated():
    # Same task, different implementation/language (Type-4) should score higher
    # than an unrelated function.
    a = "def add(a, b):\n    return a + b"
    clone = "int sum(int a, int b){\n    int r = a + b;\n    return r;\n}"
    unrelated = "def bubble_sort(x):\n    for i in range(len(x)):\n        pass"
    assert semantic.similarity(a, clone) > semantic.similarity(a, unrelated)


def test_embedding_index_query_and_pairs():
    idx = semantic.EmbeddingIndex()
    idx.add("adder_py", "def add(a, b): return a + b")
    idx.add("adder_c", "int sum(int a, int b){ return a + b; }")
    idx.add("greeter", "def greet(): print('hello world')")
    top = idx.query("int plus(int x, int y){ return x + y; }", k=1)
    assert top and top[0][0] in ("adder_py", "adder_c")
    pairs = idx.similar_pairs(threshold=-1.0)   # all pairs, ranked
    assert pairs and pairs[0][2] >= pairs[-1][2]
