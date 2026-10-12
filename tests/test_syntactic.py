"""Tests for the optional syntactic (tree-sitter) tier.

Skipped entirely when tree-sitter grammars are not installed
(``pip install pyreprism[ast]``), so the zero-dependency core is unaffected.
"""
import pytest

from PyReprism import syntactic as ast

if not ast.available():
    pytest.skip("tree-sitter grammars not installed", allow_module_level=True)


def test_available_and_supported():
    assert ast.available() is True
    assert ast.supported("python") is True
    assert ast.supported("java") is True
    assert ast.supported("not-a-language") is False


def test_cyclomatic_counts_decisions():
    # 1 (base) + if + && + for + nested if  = 5
    java = ("int f(int x){ if(x>0 && x<10){ for(int i=0;i<x;i++){ "
            "if(i%2==0) x++; } } else { return -1; } return x; }")
    assert ast.cyclomatic(java, "java") == 5


def test_cyclomatic_straight_line_is_one():
    assert ast.cyclomatic("def f(x):\n    return x + 1\n", "python") == 1


def test_functions_extracts_per_unit_complexity():
    src = ("def a(x):\n    if x: return 1\n    return 0\n\n"
           "def b(y):\n    return y\n")
    funcs = {f.name: f.cyclomatic for f in ast.functions(src, "python")}
    assert funcs.get("a") == 2      # one decision
    assert funcs.get("b") == 1      # straight line


def test_parse_unsupported_language_raises():
    with pytest.raises(ValueError):
        ast.parse("x = 1", "cobol")   # no tree-sitter mapping
