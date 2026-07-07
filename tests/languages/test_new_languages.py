"""Behavioral tests for newly implemented and migrated languages.

Each case asserts that comment markers are removed while the surrounding code
is preserved. Comparisons are whitespace-insensitive to stay robust across the
slightly different comment-stripping strategies used per language.
"""
import pytest

from PyReprism.languages.registry import LanguageRegistry
# Ensure the modules under test are imported and registered.
from PyReprism.languages import (  # noqa: F401
    html, json, yaml, pascal, prolog, protobuf, powershell, puppet, sql, sass,
    smarty, properties, opencl, makefile, markdown, vbnet, visual_basic,
)


def _norm(text):
    return ' '.join(text.split())


# (registry name, source, substrings that must remain, substrings that must be gone)
CASES = [
    ('HTML', '<p>hi</p><!-- secret -->', ['<p>hi</p>'], ['secret']),
    ('MarkDown', '# Title\n<!-- note -->\ntext', ['Title', 'text'], ['note']),
    ('Json', '{"a": 1} // trailing\n/* block */', ['"a": 1'], ['trailing', 'block']),
    ('Yaml', 'key: value # inline comment', ['key: value'], ['inline comment']),
    ('Protobuf', 'message M {} // c\n/* b */', ['message M {}'], ['// c', 'b ']),
    ('OpenCL', '__kernel void f() {} // gpu\n/* blk */', ['void f()'], ['gpu', 'blk']),
    ('Puppet', 'class x { } # note\n/* blk */', ['class x'], ['note', 'blk']),
    ('PowerShell', '$x = 1 # note\n<# block #>', ['$x = 1'], ['note', 'block']),
    ('SQL', 'SELECT 1 -- c\n/* b */ # h', ['SELECT 1'], ['-- c', 'b ', 'h']),
    ('PLSQL', 'BEGIN NULL; END; -- c\n/* b */', ['BEGIN', 'END'], ['-- c', 'b ']),
    ('Pascal', 'x := 1; // c\n(* blk *)\n{ brace }', ['x := 1;'], ['// c', 'blk', 'brace']),
    ('Prolog', 'foo :- bar. % note\n/* blk */', ['foo :- bar.'], ['note', 'blk']),
    ('Smarty', 'Hello {* hidden *} World', ['Hello', 'World'], ['hidden']),
    ('Properties', 'a=b\n# commented\n! also', ['a=b'], ['commented', 'also']),
    ('MakeFile', 'all:\n\techo hi # note', ['echo hi'], ['note']),
    ('Vbnet', "Dim x = 1 ' note", ['Dim x = 1'], ['note']),
    ('VisualBasic', "x = 1 ' note", ['x = 1'], ['note']),
    ('Sass', '.a { color: red } // note\n/* blk */', ['color: red'], ['note', 'blk']),
]


# Regression cases for languages whose comment-stripping was previously broken
# (line comments not stripped, or block comments eating surrounding code).
FIXED_REGRESSIONS = [
    ('Aspnet', 'A\n<%-- x --%>\nB', ['A', 'B'], ['x']),
    ('Aspnet', 'A\n<!-- x -->\nB', ['A', 'B'], ['x']),
    ('Autoit', 'a = 1 ; note\nb = 2', ['a = 1', 'b = 2'], ['note']),
    ('Batch', 'echo hi\nREM note\n:: also', ['echo hi'], ['note', 'also']),
    ('Basic', "x = 1 ' note\nPRINT x", ['x = 1', 'PRINT x'], ['note']),
    ('Latex', r'\a{x} % note' + '\nB', ['x', 'B'], ['note']),
    ('LiveScript', 'a = 1 # note\nb = 2', ['a = 1', 'b = 2'], ['note']),
    ('LiveScript', 'A\n/* note */\nB', ['A', 'B'], ['note']),
    ('NIM', 'var x = 1 # note\necho x', ['var x = 1', 'echo x'], ['note']),
    ('NIM', 'A\n#[ note ]#\nB', ['A', 'B'], ['note']),
    ('ObjectiveC', 'int x; // note\n/*b*/\nreturn x;', ['int x;', 'return x;'], ['note', 'b ']),
    ('Swift', 'let x = 1 // note\n/*b*/\nprint(x)', ['let x = 1', 'print(x)'], ['note', 'b ']),
    ('Less', '.a { color: red } // note\n/* blk */', ['color: red'], ['note', 'blk']),
    ('Clike', 'int x;\n/* note */\nreturn x;', ['int x;', 'return x;'], ['note']),
    ('Go', 'var x = 1\n/* note */\nreturn x', ['var x = 1', 'return x'], ['note']),
    ('Nginx', 'server 1;\nlisten 80; # note', ['server 1;', 'listen 80;'], ['note']),
    ('Ocaml', 'let a = 1\n(* note *)\nlet b = 2', ['let a = 1', 'let b = 2'], ['note']),
]


@pytest.mark.parametrize('name, source, keep, gone', CASES + FIXED_REGRESSIONS)
def test_remove_comments(name, source, keep, gone):
    cls = LanguageRegistry.get(name)
    assert cls is not None, f"{name} is not registered"
    out = cls.remove_comments(source)
    normalized = _norm(out)
    for fragment in keep:
        assert _norm(fragment) in normalized, f"{name}: expected to keep {fragment!r} in {out!r}"
    for fragment in gone:
        assert fragment not in out, f"{name}: expected to strip {fragment!r} from {out!r}"


# Cases migrated from the former root-level _test_migrated_languages.py
# (verified against the pre-existing language implementations).
MIGRATED = [
    ('MatLab', 'a = 1; % comment\nb = 2; % another', 'a = 1; b = 2;', 'if x = 1; end', 'x = 1;'),
    ('CPP', 'int x; // cmt\n/*b*/\nreturn x;', 'int x; return x;', 'if (x) return x; else x = 1;', '(x) x; x = 1;'),
    ('C', 'int x; // c\n/*b*/\nreturn 0;', 'int x; return 0;', 'if (x) return x;', '(x) x;'),
    ('Go', 'var x = 1 // c\n/*b*/\nreturn x', 'var x = 1 return x', 'if true { return }', '{ }'),
    ('Python', 'x = 1 # c\n"""doc"""\nprint(x)', 'x = 1 print(x)', 'if True: return None', ':'),
    ('Ruby', "x = 1 # c\n=begin\nblock\n=end\nputs x", 'puts x', 'if true then return end', ''),
    ('Bash', "x=1 # c\necho $x", 'x=1 echo $x', None, None),
]


@pytest.mark.parametrize('name, src, expect_no_comments, kw_src, kw_expected', MIGRATED)
def test_migrated_languages(name, src, expect_no_comments, kw_src, kw_expected):
    cls = LanguageRegistry.get(name)
    assert cls is not None, f"{name} is not registered"
    assert _norm(cls.remove_comments(src)) == _norm(expect_no_comments)
    if kw_src is not None:
        assert _norm(cls.remove_keywords(kw_src)) == _norm(kw_expected)
