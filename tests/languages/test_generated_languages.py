"""Tests for the data-driven, family-generated languages (languages/generated.py).

Beyond the shared comment-handling coverage in ``test_all_languages.py``, these
lock in the two properties most likely to regress: comment delimiters inside
string literals must be preserved, and multi-line block comments must be stripped.
"""
import pytest

import PyReprism as pr
from PyReprism.languages.generated import LANGUAGES
from PyReprism.languages.registry import LanguageRegistry

NAMES = [row[0] for row in LANGUAGES]


@pytest.mark.parametrize('name', NAMES)
def test_generated_language_is_registered(name):
    cls = LanguageRegistry.get(name)
    assert cls is not None
    assert cls.file_extension().startswith('.')
    assert isinstance(cls.keywords(), list)


@pytest.mark.parametrize('name', NAMES)
def test_resolvable_by_name_and_extension(name):
    cls = LanguageRegistry.get(name)
    assert pr.get_language(name) is cls
    assert pr.get_language(cls.file_extension()) is cls


# (language, code line whose string contains a comment delimiter that must survive)
STRING_SAFETY = [
    ('Zig', 'const s = "a // b";\n'),
    ('Solidity', 'string u = "http://x";\n'),
    ('Toml', 'url = "http://x # y"\n'),
    ('CMake', 'set(U "http://x # y")\n'),
    ('Racket', '(define s "a ; b")\n'),
    ('Elm', 's = "a -- b"\n'),
]


@pytest.mark.parametrize('name, src', STRING_SAFETY)
def test_comment_delimiter_inside_string_is_preserved(name, src):
    # The whole line is code; nothing should be removed as a comment.
    assert pr.remove_comments(src, lang=name) == src


# (language, block comment sample containing SECRET)
BLOCKS = [
    ('Vala', 'a\n/*\nzzsecret\n*/\nb\n'),
    ('Solidity', 'a\n/*\nzzsecret\n*/\nb\n'),
    ('Thrift', 'a\n/*\nzzsecret\n*/\nb\n'),
    ('Hcl', 'a\n/*\nzzsecret\n*/\nb\n'),
    ('Elm', 'a\n{-\nzzsecret\n-}\nb\n'),
    ('PureScript', 'a\n{-\nzzsecret\n-}\nb\n'),
    ('Racket', 'a\n#|\nzzsecret\n|#\nb\n'),
]


@pytest.mark.parametrize('name, src', BLOCKS)
def test_block_comments_are_stripped(name, src):
    out = pr.remove_comments(src, lang=name)
    assert 'a' in out and 'b' in out
    assert 'zzsecret' not in out


def test_zig_has_no_block_comments():
    # Zig only has // line comments; /* */ is not a comment there.
    src = 'const x = 1; /* not a comment */\n'
    assert 'not a comment' in pr.remove_comments(src, lang='Zig')


# --------------------------------------------------- nested block comments
@pytest.mark.parametrize('name', ['Odin', 'V', 'Jai'])
def test_nested_block_comments_are_fully_stripped(name):
    # A single-level regex would leave "still comment */" behind; the scanner
    # counts nesting depth and removes the whole thing.
    src = 'a := 1 /* outer /* inner */ still comment */ b := 2\n'
    out = pr.remove_comments(src, lang=name)
    assert 'a := 1' in out and 'b := 2' in out
    assert 'still comment' not in out and '*/' not in out


@pytest.mark.parametrize('name', ['Odin', 'V', 'Jai'])
def test_nested_language_string_safety(name):
    src = 'url := "http:// /* not a comment */ x"\ncode := 1\n'
    assert pr.remove_comments(src, lang=name) == src


@pytest.mark.parametrize('name', ['Odin', 'V', 'Jai'])
def test_nested_language_line_comment_and_idempotent(name):
    src = 'x := 1 // a comment\ny := 2\n'
    once = pr.remove_comments(src, lang=name)
    assert 'a comment' not in once and 'x := 1' in once
    assert pr.remove_comments(once, lang=name) == once


def test_v_extension_resolves_to_verilog_not_vlang():
    # .v is shared; Verilog wins extension lookup, V is reachable by name.
    assert pr.get_language('.v').__name__ == 'Verilog'
    assert pr.get_language('V').__name__ == 'V'


# ------------------------------------------------------- COBOL (dedicated)
COBOL_SRC = (
    "000100 IDENTIFICATION DIVISION.\n"
    "000200* THIS WHOLE LINE IS A COMMENT\n"
    "000300 PROCEDURE DIVISION.\n"
    "000400     DISPLAY 'HELLO'. *> inline comment\n"
    "000500     DISPLAY '*> inside a string stays'.\n"
)


def test_cobol_column7_and_inline_comments():
    out = pr.remove_comments(COBOL_SRC, lang='cobol')
    assert 'THIS WHOLE LINE IS A COMMENT' not in out   # column-7 comment gone
    assert 'inline comment' not in out                 # *> inline gone
    assert 'IDENTIFICATION DIVISION' in out            # code kept
    assert "DISPLAY 'HELLO'." in out


def test_cobol_star_inside_string_is_not_a_comment():
    out = pr.remove_comments(COBOL_SRC, lang='cobol')
    assert '*> inside a string stays' in out


def test_cobol_extract_and_idempotent():
    comments = pr.extract_comments(COBOL_SRC, lang='cobol')
    assert any('WHOLE LINE' in c for c in comments)
    assert any('inline comment' in c for c in comments)
    once = pr.remove_comments(COBOL_SRC, lang='cobol')
    assert pr.remove_comments(once, lang='cobol') == once


def test_cobol_slash_in_column7_is_comment():
    # A '/' in the indicator column is a page-eject comment line.
    src = "000100 DISPLAY 'A'.\n000200/ PAGE EJECT LINE\n000300 DISPLAY 'B'.\n"
    out = pr.remove_comments(src, lang='cobol')
    assert 'PAGE EJECT LINE' not in out
    assert "DISPLAY 'A'." in out and "DISPLAY 'B'." in out
