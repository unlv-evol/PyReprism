"""Tests for batch/directory processing (discovery, analyze, transform, CLI scan)."""
import json

import pytest

from PyReprism import batch
from PyReprism.cli import main


@pytest.fixture
def tree(tmp_path):
    (tmp_path / 'sub').mkdir()
    (tmp_path / '.git').mkdir()
    (tmp_path / 'node_modules').mkdir()
    (tmp_path / 'a.py').write_text('def f():\n    return 1  # c\n')
    (tmp_path / 'sub' / 'b.py').write_text('x = 2  # c\ny = 3\n')
    (tmp_path / 'sub' / 'm.c').write_text('int main(){return 0;} // c\n')
    (tmp_path / '.git' / 'junk.py').write_text('secret = 1\n')          # skipped dir
    (tmp_path / 'node_modules' / 'dep.js').write_text('var x = 1\n')    # skipped dir
    (tmp_path / 'readme.zzz').write_text('not source\n')               # unknown ext
    return tmp_path


# -------------------------------------------------------------------- discovery
def test_discovery_skips_junk_and_unknown(tree):
    found = sorted(p.name for _base, p, _cls in batch.iter_source_files(tree))
    assert found == ['a.py', 'b.py', 'm.c']


def test_discovery_non_recursive(tree):
    found = sorted(p.name for _b, p, _c in batch.iter_source_files(tree, recursive=False))
    assert found == ['a.py']


def test_discovery_include_exclude(tree):
    only_py = sorted(p.name for _b, p, _c in batch.iter_source_files(tree, include=['*.py']))
    assert only_py == ['a.py', 'b.py']
    no_b = sorted(p.name for _b, p, _c in batch.iter_source_files(tree, exclude=['b.py']))
    assert no_b == ['a.py', 'm.c']


def test_py_detected_as_python(tree):
    langs = {p.name: cls.__name__ for _b, p, cls in batch.iter_source_files(tree)}
    assert langs['a.py'] == 'Python'          # not Django (canonical preference)
    assert langs['m.c'] == 'C'


# ---------------------------------------------------------------------- analyze
def test_analyze_totals_and_by_language(tree):
    report = batch.analyze(tree)
    totals = report.totals()
    assert totals['files'] == 3
    assert totals['code_lines'] == 5
    langs = report.by_language()
    assert langs['Python']['files'] == 2
    assert langs['C']['files'] == 1


def test_analyze_json_and_csv(tree):
    report = batch.analyze(tree)
    data = json.loads(report.to_json())
    assert set(data) == {'files', 'by_language', 'totals'}
    assert len(data['files']) == 3
    csv_text = report.to_csv()
    assert csv_text.splitlines()[0].startswith('path,language,lines')
    assert len(csv_text.splitlines()) == 4  # header + 3 files


# -------------------------------------------------------------------- transform
def test_transform_to_output_mirror(tree, tmp_path):
    out = tmp_path.parent / 'out'
    results = batch.transform(tree, lambda text, cls: cls.remove_comments(text), output=out)
    assert len(results) == 3
    assert (out / 'a.py').exists()
    assert (out / 'sub' / 'b.py').exists()
    assert '# c' not in (out / 'a.py').read_text()


def test_transform_in_place(tree):
    batch.transform(tree, lambda text, cls: cls.remove_comments(text), in_place=True)
    assert '# c' not in (tree / 'a.py').read_text()


def test_transform_collect_results(tree):
    results = batch.transform(tree, lambda text, cls: cls.remove_comments(text))
    # no output/in_place -> returns (path, transformed_text)
    assert all(isinstance(text, str) for _path, text in results)


# --------------------------------------------------------------------------- CLI
def test_cli_scan_text(tree, capsys):
    assert main(['scan', str(tree)]) == 0
    out = capsys.readouterr().out
    assert 'Python' in out and 'C' in out
    assert '3 files' in out


def test_cli_scan_json(tree, capsys):
    assert main(['scan', str(tree), '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['totals']['files'] == 3


def test_cli_scan_csv(tree, capsys):
    assert main(['scan', str(tree), '--csv']) == 0
    assert capsys.readouterr().out.splitlines()[0].startswith('path,language')


def test_cli_directory_transform_output(tree, tmp_path, capsys):
    out = tmp_path.parent / 'cliout'
    assert main(['remove', 'comments', str(tree), '--output', str(out)]) == 0
    assert (out / 'a.py').exists()
    assert '# c' not in (out / 'a.py').read_text()


def test_cli_count_over_directory(tree, capsys):
    assert main(['count', 'comments', str(tree)]) == 0
    out = capsys.readouterr().out
    # per-file labelled output because a directory expands to many files
    assert out.count('\t') == 3
