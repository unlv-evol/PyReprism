"""Tests for stats(), normalize(), blank_comments() and complexity metrics."""
import json

import pytest

import PyReprism as pr
from PyReprism.languages import _load_all_languages
from PyReprism.languages.registry import LanguageRegistry
from PyReprism.metrics import CodeStats, Halstead
from PyReprism.cli import main

_load_all_languages()

SRC = '''# header
def add(price, qty):
    total = price * qty + 42   # inline
    label = "cost"
    return total

'''


# ------------------------------------------------------------------------ stats
def test_stats_line_classification():
    s = pr.stats(SRC, lang='python')
    assert isinstance(s, CodeStats)
    assert s.lines == 6           # trailing blank line dropped by splitlines
    assert s.code_lines == 4
    assert s.comment_lines == 1
    assert s.blank_lines == 1
    assert s.lines == s.code_lines + s.comment_lines + s.blank_lines


def test_stats_token_counts_and_ratios():
    s = pr.stats(SRC, lang='python')
    assert s.comment_tokens == 2
    assert s.string_tokens == 1
    assert s.number_tokens == 1
    assert s.keyword_tokens == 2          # def, return
    assert s.comment_to_code_ratio == pytest.approx(0.25)
    assert 'comment_density' in s.as_dict()


def test_stats_block_comment_with_trailing_code_counts_as_code():
    # line 1 has both code and a comment -> counts as a code line, not comment
    s = pr.stats('x = 1  # c\n', lang='python')
    assert s.code_lines == 1
    assert s.comment_lines == 0


# -------------------------------------------------------------------- normalize
def test_normalize_defaults():
    out = pr.normalize('total = price * 42  # c\n', lang='python')
    assert '# c' not in out
    assert '42' not in out and '0' in out      # number masked
    assert 'VAR1' in out and 'VAR2' in out     # identifiers renamed
    assert 'price' not in out


def test_normalize_consistent_identifier_mapping():
    out = pr.normalize('a = b + a', lang='python', mask_numbers=False)
    # 'a' -> VAR1 both times, 'b' -> VAR2
    assert out == 'VAR1 = VAR2 + VAR1'


def test_normalize_keeps_keywords():
    out = pr.normalize('def foo(): return 1', lang='python')
    assert out.startswith('def ')
    assert 'return' in out


def test_normalize_toggles():
    src = 'x = "hi" + 3'
    assert '"hi"' in pr.normalize(src, lang='python', mask_strings=False)
    assert '3' in pr.normalize(src, lang='python', mask_numbers=False)
    assert 'x' in pr.normalize(src, lang='python', rename_identifiers=False)


def test_normalize_collapse_whitespace():
    assert pr.normalize('a   =    b', lang='python', collapse_whitespace=True) == 'VAR1 = VAR2'


# ---------------------------------------------------------------- blank_comments
def test_blank_comments_preserves_line_count():
    src = 'a = 1  // secret\nb = 2\n/* x\n y */\nc = 3\n'
    out = pr.blank_comments(src, lang='clike')
    assert 'secret' not in out
    assert out.count('\n') == src.count('\n')      # line numbers stable
    assert 'a = 1' in out and 'c = 3' in out


def test_blank_comments_empty_replacement():
    out = pr.blank_comments('x = 1 # c\n', lang='python', replacement='')
    assert out == 'x = 1 \n'


# ---------------------------------------------------------------------- registry
def test_stats_and_normalize_work_for_all_languages():
    from PyReprism.languages.registry import LanguageRegistry
    sample = 'a = 1 + 2 // c\n# h\nname = "x"\n'
    for name, cls in LanguageRegistry.all().items():
        s = cls.stats(sample)
        assert s.lines >= 1
        assert isinstance(cls.normalize(sample), str)


# --------------------------------------------------------------------------- CLI
def test_cli_stats_json(monkeypatch, capsys):
    import io
    monkeypatch.setattr('sys.stdin', io.StringIO('# c\nx = 1\n'))
    assert main(['stats', '--lang', 'python', '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['comment_lines'] == 1 and data['code_lines'] == 1


def test_cli_normalize(monkeypatch, capsys):
    import io
    monkeypatch.setattr('sys.stdin', io.StringIO('total = price * 42\n'))
    assert main(['normalize', '--lang', 'python']) == 0
    out = capsys.readouterr().out
    assert 'VAR1' in out and '0' in out and 'price' not in out


def test_cli_normalize_keep_flags(monkeypatch, capsys):
    import io
    monkeypatch.setattr('sys.stdin', io.StringIO('total = 42\n'))
    assert main(['normalize', '--lang', 'python', '--keep-names', '--keep-numbers']) == 0
    assert capsys.readouterr().out.strip() == 'total = 42'


# ------------------------------------------------------------------- halstead
def test_halstead_counts_and_derived():
    h = pr.halstead('x = a + b * a', lang='python')
    assert isinstance(h, Halstead)
    assert h.total_operators >= 1 and h.total_operands >= 1
    # 'a' appears twice -> counted once as a distinct operand
    assert h.distinct_operands < h.total_operands
    assert h.volume > 0 and h.difficulty > 0
    assert set(h.as_dict()) >= {'volume', 'difficulty', 'effort', 'bugs', 'vocabulary'}


def test_halstead_empty_source_is_zero():
    h = pr.halstead('', lang='python')
    assert h.volume == 0.0 and h.difficulty == 0.0


# ---------------------------------------------------------------- cyclomatic
def test_cyclomatic_straightline_is_one():
    assert pr.cyclomatic_complexity('x = 1\ny = 2\n', lang='python') == 1


def test_cyclomatic_counts_branches_and_boolean_ops():
    # base 1 + if + and + elif + for = 5
    src = 'def f(n):\n    if n > 0 and n < 9:\n        return 1\n    elif n:\n        for i in n:\n            pass\n'
    assert pr.cyclomatic_complexity(src, lang='python') == 5


def test_cyclomatic_counts_c_style_operators():
    # base 1 + if + && + ternary ?
    assert pr.cyclomatic_complexity('if (a && b) return x ? y : z;', lang='c') == 4


# ---------------------------------------------------------------- nesting / MI
def test_max_nesting_depth():
    py = LanguageRegistry.get('Python')
    assert py.max_nesting_depth('f(g(h(x)))') == 3
    assert py.max_nesting_depth('a + b') == 0


def test_maintainability_index_range_and_ordering():
    simple = pr.maintainability_index('x = 1\n', lang='python')
    complex_src = ('def f(a, b, c, d):\n' + '    if a and b or c and d:\n'
                   '        return a * b + c - d / a\n' * 3)
    hard = pr.maintainability_index(complex_src, lang='python')
    assert 0 <= hard <= simple <= 100


def test_code_metrics_bundles_everything():
    m = pr.code_metrics('def f():\n    return 1  # c\n', lang='python')
    assert 'code_lines' in m and 'halstead' in m
    assert 'cyclomatic_complexity' in m and 'maintainability_index' in m
    assert 'max_nesting_depth' in m


# ------------------------------------------------------- works for every language
def test_complexity_metrics_run_for_all_languages():
    sample = 'a = 1\nif a and b:\n    f(g(x))\n'
    for name, cls in LanguageRegistry.all().items():
        assert cls.cyclomatic_complexity(sample) >= 1
        assert cls.max_nesting_depth(sample) >= 0
        assert 0 <= cls.maintainability_index(sample) <= 100
        assert cls.halstead(sample).length >= 0


# --------------------------------------------------------------------------- CLI
def test_cli_stats_full(monkeypatch, capsys):
    import io
    monkeypatch.setattr('sys.stdin', io.StringIO('if (a && b) { return 1; }\n'))
    assert main(['stats', '--lang', 'c', '--full', '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['cyclomatic_complexity'] >= 2
    assert 'volume' in data['halstead']
    assert 'maintainability_index' in data
