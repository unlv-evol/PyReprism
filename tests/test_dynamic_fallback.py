"""Tests for the Pygments long-tail fallback (languages/dynamic.py).

When a language/extension is not one of the built-in modules, and Pygments is
installed, resolution falls back to a Pygments-backed language. These tests are
skipped when Pygments is not available (the fallback returns ``None`` and the
public API raises ``ValueError`` as before).

Standard ML (``.sml``) is used as the exemplar: it has no built-in PyReprism
module but Pygments ships a lexer for it.
"""
import pytest

import PyReprism as pr
from PyReprism.languages.dynamic import pygments_language_for

pytest.importorskip('pygments')


def test_unknown_language_resolves_via_pygments():
    cls = pr.get_language('.sml')  # Standard ML: no built-in module
    assert cls is not None
    assert getattr(cls, 'pygments_backed', False) is True


def test_fallback_strips_and_extracts_comments():
    src = 'val x = 1 (* a comment *)\nval y = 2\n'
    out = pr.remove_comments(src, lang='.sml')
    assert 'val x = 1' in out and 'val y = 2' in out
    assert 'a comment' not in out
    assert any('a comment' in c for c in pr.extract_comments(src, lang='sml'))


def test_fallback_does_not_override_builtins():
    # A built-in language must resolve to its zero-dependency module, not Pygments.
    zig = pr.get_language('Zig')
    assert getattr(zig, 'pygments_backed', False) is False


def test_pygments_language_for_returns_none_for_nonsense():
    assert pygments_language_for('definitely-not-a-real-language-xyz') is None


def test_fallback_tokenizes_with_comment_token():
    toks = pr.tokenize('val x = 1 (* c *)\n', lang='sml')
    assert any(t.type.name == 'COMMENT' for t in toks)
