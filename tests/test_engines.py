"""Tests for the tokenization backends (regex default, optional pygments)."""
import pytest

import PyReprism as pr
from PyReprism.engines import RegexEngine, get_engine

pygments = pytest.importorskip("pygments")  # skip this module if pygments is absent


# ------------------------------------------------------------------- engine selection
def test_get_engine_regex_default():
    assert isinstance(get_engine(), RegexEngine)
    assert isinstance(get_engine('regex'), RegexEngine)


def test_get_engine_auto_prefers_pygments_when_available():
    assert type(get_engine('auto')).__name__ == 'PygmentsEngine'


def test_get_engine_unknown():
    with pytest.raises(ValueError):
        get_engine('nope')


# --------------------------------------------------------------------- correctness win
def test_pygments_does_not_treat_hash_in_string_as_comment():
    # regex engine may mis-handle this; pygments understands the string.
    src = 'url = "http://x#frag"  # real\nx = 1\n'
    out = pr.remove_comments(src, lang='python', engine='pygments')
    assert '"http://x#frag"' in out       # string preserved intact
    assert '# real' not in out            # actual comment removed


def test_pygments_extract_strings_whole_literals():
    src = 's = "a#b"\n'
    assert pr.extract_strings(src, lang='python', engine='pygments') == ['"a#b"']


def test_pygments_extract_comments():
    src = '# top\ncode = 1  # side\n'
    assert pr.extract_comments(src, lang='python', engine='pygments') == ['# top', '# side']


# ------------------------------------------------------------------------- lossless
@pytest.mark.parametrize('lang', ['python', 'java', 'javascript', 'go', 'c', 'ruby'])
def test_pygments_tokenize_is_lossless(lang):
    src = 'x = 1 + 2  // c\n# h\nname = "hi"\nreturn x\n'
    toks = pr.tokenize(src, lang=lang, engine='pygments')
    assert ''.join(t.value for t in toks) == src


# ------------------------------------------------------------------------- parity
def test_engine_derived_ops_agree_with_lossless_join():
    # For a token-derived engine, remove_comments == join of non-comment tokens.
    src = 'def f():\n    return 40 + 2  # c\n'
    toks = pr.tokenize(src, lang='python', engine='pygments')
    expected = ''.join(t.value for t in toks if t.type.value != 'comment')
    assert pr.remove_comments(src, lang='python', engine='pygments') == expected


def test_normalize_and_stats_via_pygments():
    src = 'total = price * 42  # c\n'
    assert pr.normalize(src, lang='python', engine='pygments') == 'VAR1 = VAR2 * 0  \n'
    s = pr.stats(src, lang='python', engine='pygments')
    assert s.comment_lines == 0 and s.code_lines == 1


def test_preprocess_with_engine():
    src = 's = "x" + 3  # c\n'
    out = pr.preprocess(src, lang='python', steps=['comments', 'strings', 'numbers'],
                        engine='pygments')
    assert '"x"' not in out and '3' not in out and '# c' not in out


# ------------------------------------------------------------------------------ CLI
def test_cli_engine_flag(monkeypatch, capsys):
    import io
    from PyReprism.cli import main
    monkeypatch.setattr('sys.stdin', io.StringIO('u = "a#b"  # c\n'))
    assert main(['remove', 'comments', '--lang', 'python', '--engine', 'pygments']) == 0
    out = capsys.readouterr().out
    assert '"a#b"' in out and '# c' not in out
