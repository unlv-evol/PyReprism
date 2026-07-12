"""Tests for fingerprinting and clone/plagiarism similarity."""
import pytest

from PyReprism import fingerprints as fp
from PyReprism.languages import _load_all_languages
from PyReprism.languages.registry import LanguageRegistry
from PyReprism.cli import main

_load_all_languages()

ORIGINAL = "def total(items):\n    s = 0\n    for x in items:\n        s = s + x\n    return s\n"
# same structure, renamed identifiers + changed literal -> Type-2 clone
RENAMED = "def sum_all(values):\n    acc = 1\n    for v in values:\n        acc = acc + v\n    return acc\n"
UNRELATED = "class Foo:\n    def bar(self):\n        print('hello there world')\n"


# --------------------------------------------------------------- fingerprint
def test_fingerprint_is_deterministic():
    assert fp.fingerprint(ORIGINAL, 'python') == fp.fingerprint(ORIGINAL, 'python')
    assert all(isinstance(h, int) for h in fp.fingerprint(ORIGINAL, 'python'))


def test_empty_source_has_empty_fingerprint():
    assert fp.fingerprint('', 'python') == set()


# ---------------------------------------------------------------- similarity
def test_identical_similarity_is_one():
    assert fp.similarity(ORIGINAL, ORIGINAL, 'python') == 1.0


def test_renamed_clone_is_detected_with_normalization():
    # default normalize=True makes it rename/literal invariant
    assert fp.similarity(ORIGINAL, RENAMED, 'python') > 0.9


def test_unrelated_code_is_dissimilar():
    assert fp.similarity(ORIGINAL, UNRELATED, 'python') < 0.3


def test_no_normalize_is_sensitive_to_renaming():
    with_norm = fp.similarity(ORIGINAL, RENAMED, 'python', normalize=True)
    without = fp.similarity(ORIGINAL, RENAMED, 'python', normalize=False)
    assert without < with_norm


def test_containment_is_asymmetric_fraction():
    assert fp.containment(ORIGINAL, RENAMED, 'python') > 0.9
    assert fp.containment('', ORIGINAL, 'python') == 0.0


def test_jaccard_edge_cases():
    assert fp.jaccard(set(), set()) == 1.0
    assert fp.jaccard({1}, set()) == 0.0
    assert fp.jaccard({1, 2}, {2, 3}) == pytest.approx(1 / 3)


# --------------------------------------------------------------------- index
def test_index_similar_pairs():
    idx = fp.FingerprintIndex(k=4, w=3)
    idx.add('a', ORIGINAL, 'python')
    idx.add('b', RENAMED, 'python')
    idx.add('c', UNRELATED, 'python')
    pairs = idx.similar_pairs(threshold=0.5)
    assert [(a, b) for a, b, _ in pairs] == [('a', 'b')]
    assert idx.matches('a', threshold=0.5)[0][0] == 'b'


def test_index_add_paths(tmp_path):
    (tmp_path / 'x.py').write_text(ORIGINAL)
    (tmp_path / 'y.py').write_text(RENAMED)
    (tmp_path / 'z.py').write_text(UNRELATED)
    idx = fp.FingerprintIndex(k=4, w=3)
    idx.add_paths(tmp_path)
    assert len(idx.prints) == 3
    pairs = idx.similar_pairs(threshold=0.5)
    assert len(pairs) == 1 and pairs[0][2] > 0.9


# ---------------------------------------------------- works for all languages
def test_fingerprint_runs_for_all_languages():
    sample = 'a = f(x) + g(y)\nb = f(x) + g(y)\n'
    for name, cls in LanguageRegistry.all().items():
        assert isinstance(fp.fingerprint(sample, cls), set)


# --------------------------------------------------------------------------- CLI
def test_cli_similarity(tmp_path, capsys):
    a = tmp_path / 'a.py'
    b = tmp_path / 'b.py'
    a.write_text(ORIGINAL)
    b.write_text(RENAMED)
    assert main(['similarity', str(a), str(b)]) == 0
    assert float(capsys.readouterr().out.strip()) > 0.9


def test_cli_clones(tmp_path, capsys):
    (tmp_path / 'a.py').write_text(ORIGINAL)
    (tmp_path / 'b.py').write_text(RENAMED)
    (tmp_path / 'c.py').write_text(UNRELATED)
    assert main(['clones', str(tmp_path), '--threshold', '0.5']) == 0
    out = capsys.readouterr().out
    assert 'a.py' in out and 'b.py' in out and 'c.py' not in out
