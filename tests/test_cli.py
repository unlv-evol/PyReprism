"""Tests for the pyreprism command-line interface."""
import json

import pytest

from PyReprism.cli import main


def run(argv, stdin=None, monkeypatch=None, capsys=None):
    """Invoke the CLI, returning (exit_code, stdout, stderr)."""
    if stdin is not None:
        import io
        monkeypatch.setattr('sys.stdin', io.StringIO(stdin))
    code = main(argv)
    out, err = capsys.readouterr()
    return code, out, err


def test_remove_comments_stdin(monkeypatch, capsys):
    code, out, err = run(['remove', 'comments', '--lang', 'python'],
                         stdin='x = 1  # c\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert '# c' not in out
    assert 'x = 1' in out


def test_remove_comments_file_autodetect(tmp_path, monkeypatch, capsys):
    f = tmp_path / 'a.py'
    f.write_text('y = 2  # note\n')
    code, out, err = run(['remove', 'comments', str(f)], monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert 'note' not in out
    assert 'y = 2' in out


def test_remove_in_place(tmp_path, monkeypatch, capsys):
    f = tmp_path / 'b.py'
    f.write_text('z = 3  # gone\n')
    # Options go after positionals: argparse on Python <= 3.11 only matches
    # positionals in the first contiguous block, so a flag between the construct
    # and the path would drop the path ("unrecognized arguments").
    code, out, err = run(['remove', 'comments', str(f), '--in-place'],
                         monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert 'gone' not in f.read_text()
    assert out == ''  # nothing to stdout in in-place mode


def test_count_comments(monkeypatch, capsys):
    code, out, err = run(['count', 'comments', '--lang', 'python'],
                         stdin='# a\ncode\n# b\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert out.strip() == '2'


def test_extract_comments_json(monkeypatch, capsys):
    code, out, err = run(['extract', 'comments', '--lang', 'python', '--json'],
                         stdin='# a\ncode  # b\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert json.loads(out) == ['# a', '# b']


def test_extract_numbers(monkeypatch, capsys):
    code, out, err = run(['extract', 'numbers', '--lang', 'python'],
                         stdin='a = 5 + 42\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert out.split() == ['5', '42']


def test_preprocess_steps(monkeypatch, capsys):
    code, out, err = run(['preprocess', '--steps', 'comments,whitespace', '--lang', 'python'],
                         stdin='# c\nx = 5 + 6\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert out.strip() == 'x=5+6'


def test_tokenize_json(monkeypatch, capsys):
    code, out, err = run(['tokenize', '--lang', 'clike', '--json'],
                         stdin='x=5', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    types = [t['type'] for t in json.loads(out)]
    assert 'identifier' in types and 'number' in types


def test_languages_lists_many(monkeypatch, capsys):
    code, out, err = run(['languages'], monkeypatch=monkeypatch, capsys=capsys)
    assert code == 0
    assert 'Python' in out
    assert out.count('\n') > 100


def test_no_language_errors(monkeypatch, capsys):
    with pytest.raises(SystemExit) as excinfo:
        run(['count', 'comments'], stdin='x\n', monkeypatch=monkeypatch, capsys=capsys)
    assert excinfo.value.code == 2


def test_unknown_language_errors(monkeypatch, capsys):
    code, out, err = run(['count', 'comments', '--lang', 'nope'],
                         stdin='x\n', monkeypatch=monkeypatch, capsys=capsys)
    assert code == 2
    assert 'Unknown language' in err


def test_version(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(['--version'])
    assert excinfo.value.code == 0
    assert 'pyreprism' in capsys.readouterr().out
