"""Tests for language detection (filename, shebang, content)."""
import io

import pytest

import PyReprism as pr
from PyReprism.cli import main


# ----------------------------------------------------------------- by filename
def test_detect_by_filename():
    assert pr.detect_language(filename="main.go").__name__ == 'Go'
    assert pr.detect_language(filename="a/b/c.rs").__name__ == 'Rust'


def test_detect_filename_unknown_returns_none():
    assert pr.detect_language(filename="notes.zzz") is None


def test_detect_py_is_python_not_django():
    assert pr.detect_language(filename="script.py").__name__ == 'Python'


# ------------------------------------------------------------------- by shebang
@pytest.mark.parametrize('shebang, expected', [
    ('#!/usr/bin/env python3\n', 'Python'),
    ('#!/usr/bin/python\n', 'Python'),
    ('#!/usr/bin/env node\n', 'JavaScript'),
    ('#!/usr/bin/ruby\n', 'Ruby'),
    ('#!/usr/bin/perl\n', 'Perl'),
    ('#!/bin/bash\n', 'Bash'),
    ('#!/bin/sh\n', 'Bash'),
])
def test_detect_by_shebang(shebang, expected):
    assert pr.detect_language(source=shebang + 'code here\n').__name__ == expected


def test_detect_shebang_takes_priority_over_content():
    # Even if the body looks like something else, the shebang wins.
    src = '#!/usr/bin/env python\nint main() { return 0; }\n'
    assert pr.detect_language(source=src).__name__ == 'Python'


def test_filename_takes_priority_over_shebang():
    src = '#!/usr/bin/env python\ncode\n'
    assert pr.detect_language(filename="x.rb", source=src).__name__ == 'Ruby'


# -------------------------------------------------------------------- no signal
def test_detect_plain_text_is_none():
    assert pr.detect_language(source="just prose, nothing code-like at all") is None


def test_detect_nothing_returns_none():
    assert pr.detect_language() is None


# -------------------------------------------------------------------------- CLI
def test_cli_stdin_autodetects_from_shebang(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('#!/usr/bin/env python\nx = 1  # c\n'))
    assert main(['remove', 'comments']) == 0     # no --lang
    out = capsys.readouterr().out
    assert '# c' not in out and 'x = 1' in out


def test_cli_stdin_without_signal_errors(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('plain prose\n'))
    with pytest.raises(SystemExit) as excinfo:
        main(['remove', 'comments'])
    assert excinfo.value.code == 2
