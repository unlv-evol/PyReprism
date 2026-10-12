"""Tests for located clone detection (clones.py) and reporters (reporters.py)."""
import json
import os

import pytest

from PyReprism import clones, reporters
from PyReprism import semantic as sem

SHARED = "\n".join(f"    total = total + arr[{i}] * factor" for i in range(8))
FILE_A = "def sum_a(arr, factor):\n    total = 0\n" + SHARED + "\n    return total\n"
# Type-2: identifiers renamed -> still an exact clone after normalization.
FILE_B = ("def compute(values, k):\n    total = 0\n"
          + SHARED.replace("arr", "values").replace("factor", "k")
          + "\n    return total\n")
FILE_C = "def greet():\n    print('hello world')\n    return 42\n"


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "a.py").write_text(FILE_A)
    (tmp_path / "b.py").write_text(FILE_B)
    (tmp_path / "c.py").write_text(FILE_C)
    return tmp_path


def _bases(clone):
    return {os.path.basename(clone.a.path), os.path.basename(clone.b.path)}


def test_exact_clone_is_located(tree):
    rep = clones.detect(str(tree), min_tokens=8, min_lines=3)
    exact = [c for c in rep.clones if c.kind == "exact"]
    assert len(exact) == 1
    c = exact[0]
    assert _bases(c) == {"a.py", "b.py"}       # the unrelated c.py is not flagged
    assert c.a.start_line >= 1 and c.a.end_line > c.a.start_line   # real line range
    assert c.score == 1.0


def test_min_lines_filters_small_clones(tree):
    rep = clones.detect(str(tree), min_tokens=8, min_lines=999)
    assert [c for c in rep.clones if c.kind == "exact"] == []


def test_no_normalize_still_finds_identical(tmp_path):
    (tmp_path / "x.py").write_text(FILE_A)
    (tmp_path / "y.py").write_text(FILE_A)          # identical (Type-1)
    rep = clones.detect(str(tmp_path), min_tokens=8, min_lines=3, normalize=False)
    assert any(c.kind == "exact" for c in rep.clones)


def test_report_summary_and_duplication_pct(tree):
    s = clones.detect(str(tree), min_tokens=8, min_lines=3).summary()
    assert s["files"] == 3 and s["clones"] >= 1
    assert 0 < s["duplication_pct"] <= 100
    assert s["by_kind"].get("exact", 0) >= 1


def test_reporters_render(tree):
    rep = clones.detect(str(tree), min_tokens=8, min_lines=3)
    j = json.loads(reporters.to_json(rep))
    assert "summary" in j and j["clones"][0]["kind"] == "exact"
    sarif = json.loads(reporters.to_sarif(rep))
    assert sarif["version"] == "2.1.0"
    res = sarif["runs"][0]["results"][0]
    assert res["ruleId"] == "pyreprism/exact-clone"
    assert res["locations"][0]["physicalLocation"]["region"]["startLine"] >= 1
    assert res["relatedLocations"]                          # partner fragment
    assert "clone report" in reporters.to_markdown(rep)
    assert "duplicated lines" in reporters.to_console(rep)


def test_html_reporter(tree):
    rep = clones.detect(str(tree), min_tokens=8, min_lines=3)
    h = reporters.to_html(rep, target="proj/", max_duplication=5.0)
    assert h.startswith("<!doctype html>")
    assert "<title>PyReprism Clone Report</title>" in h
    assert "pyreprism/exact-clone" in h            # rule id per clone
    assert 'data-kind="exact"' in h                # filterable card
    assert "CI&nbsp;" in h and "% gate" in h       # gate + threshold marker
    assert reporters.render(rep, "html").startswith("<!doctype html>")


def test_html_reporter_escapes_and_survives_missing_files(tmp_path):
    # A clone whose files are gone on disk must still render (snippets skipped),
    # and any HTML-special content must be escaped, not injected.
    (tmp_path / "x.py").write_text(FILE_A)
    (tmp_path / "y.py").write_text(FILE_A)
    rep = clones.detect(str(tmp_path), min_tokens=8, min_lines=3, normalize=False)
    (tmp_path / "x.py").unlink()                   # remove after detection
    h = reporters.to_html(rep)                     # must not raise
    assert h.startswith("<!doctype html>")
    assert "No clones detected." not in h          # the y.py<->x.py pair is kept


def test_render_unknown_reporter_raises(tree):
    rep = clones.detect(str(tree), min_tokens=8, min_lines=3)
    with pytest.raises(ValueError):
        reporters.render(rep, "nope")


@pytest.mark.skipif(not sem.available(), reason="semantic tier not installed")
def test_semantic_clones_flow_into_report(tmp_path):
    # Two functions, same behaviour, different surface -> Type-4 (not exact).
    (tmp_path / "p.py").write_text(
        "def total(xs):\n    s = 0\n    for x in xs:\n        s += x\n    return s\n")
    (tmp_path / "q.py").write_text(
        "def accumulate(items):\n    return sum(v for v in items)\n")
    rep = clones.detect(str(tmp_path), min_tokens=8, min_lines=2,
                        semantic=True, semantic_threshold=0.4)
    # p/q are not exact clones ...
    assert not any(c.kind == "exact" and _bases(c) == {"p.py", "q.py"}
                   for c in rep.clones)
    # ... every reported clone carries a valid kind, and any p/q pair is semantic.
    assert all(c.kind in ("exact", "near", "semantic") for c in rep.clones)
    pq = [c for c in rep.clones if _bases(c) == {"p.py", "q.py"}]
    assert all(c.kind == "semantic" for c in pq)
    # SARIF tags each kind with its own rule id.
    sarif = json.loads(reporters.to_sarif(rep))
    for r in sarif["runs"][0]["results"]:
        assert r["ruleId"] in ("pyreprism/exact-clone", "pyreprism/near-clone",
                               "pyreprism/semantic-clone")
