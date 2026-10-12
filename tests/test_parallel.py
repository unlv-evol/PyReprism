"""Parallel processing returns the same results as serial runs."""
import pytest

from PyReprism import _parallel, batch, clones
from PyReprism.cli import main
from PyReprism.languages import get_language_by_extension
from PyReprism.tokens import Token, TokenType

SOURCES = {
    'py': 'def f(x):\n    """Doc."""\n    if x and x > 1:  # c\n        return x\n    return 0\n',
    'js': 'function g(a) {\n  // c\n  return a ? `t/${a}` : "u//v";\n}\n',
    'java': 'class A {\n  /* c */\n  int f(int x) { return x > 0 ? x : -x; }\n}\n',
    'h': '#include "a/b.h"\nint h(void); // c\n',
}


@pytest.fixture
def tree(tmp_path, monkeypatch):
    # Enough files to cross the threshold at which work is sent to processes.
    monkeypatch.setattr(_parallel, 'MIN_PARALLEL_ITEMS', 4)
    for i in range(12):
        for ext, src in SOURCES.items():
            (tmp_path / f'f{i}.{ext}').write_text(src * (1 + i % 3))
    return tmp_path


def _square(x):
    return x * x


def test_pmap_keeps_order_and_matches_serial(monkeypatch):
    monkeypatch.setattr(_parallel, 'MIN_PARALLEL_ITEMS', 4)
    assert _parallel.pmap(_square, range(50), jobs=2) == [x * x for x in range(50)]


def test_resolve_jobs():
    assert _parallel.resolve_jobs(1) == 1
    assert _parallel.resolve_jobs(0) >= 1
    assert _parallel.resolve_jobs(None) == _parallel.resolve_jobs(0)


def test_analyze_parallel_equals_serial(tree):
    assert batch.analyze(tree, jobs=2).to_dict() == batch.analyze(tree, jobs=1).to_dict()


def _metrics(src, lang):
    return lang.code_metrics(src)


def test_map_files_parallel_equals_serial(tree):
    serial = batch.map_files(tree, _metrics, jobs=1)
    parallel = batch.map_files(tree, _metrics, jobs=2)
    assert [(p, c, r) for p, c, r in parallel] == [(p, c, r) for p, c, r in serial]
    assert len(serial) == 12 * len(SOURCES)


def _upper(src, _lang):
    return src.upper()


def test_transform_parallel_equals_serial(tree, tmp_path_factory):
    a, b = tmp_path_factory.mktemp('a'), tmp_path_factory.mktemp('b')
    batch.transform(tree, _upper, output=a, jobs=1)
    batch.transform(tree, _upper, output=b, jobs=2)
    files = sorted(p.relative_to(a) for p in a.rglob('*') if p.is_file())
    assert files == sorted(p.relative_to(b) for p in b.rglob('*') if p.is_file())
    assert all((a / f).read_text() == (b / f).read_text() for f in files)


@pytest.mark.parametrize('normalize', [True, False])
def test_clones_parallel_equals_serial(tree, normalize):
    s = clones.detect(str(tree), normalize=normalize, min_tokens=10, min_lines=2, jobs=1)
    p = clones.detect(str(tree), normalize=normalize, min_tokens=10, min_lines=2, jobs=2)
    assert [c.as_dict() for c in p.clones] == [c.as_dict() for c in s.clones]
    assert p.summary() == s.summary()


def test_cli_jobs_option(tree, capsys):
    assert main(['scan', str(tree), '-j', '1']) == 0
    serial = capsys.readouterr().out
    assert main(['scan', str(tree), '--jobs', '2']) == 0
    assert capsys.readouterr().out == serial


@pytest.mark.parametrize('ext, name', [('.h', 'C'), ('.hpp', 'CPP'), ('.cc', 'CPP'),
                                       ('.mjs', 'JavaScript'), ('.yml', 'Yaml'),
                                       ('.pyi', 'Python'), ('.py', 'Python'),
                                       ('.v', 'Verilog')])
def test_secondary_extensions(ext, name):
    assert get_language_by_extension(ext).__name__ == name


def test_token_is_immutable_and_keeps_its_fields():
    tok = Token(TokenType.STRING, '"a"', 0, 3, 1)
    assert (tok.type, tok.value, tok.start, tok.end, tok.line) == (TokenType.STRING, '"a"', 0, 3, 1)
    with pytest.raises(AttributeError):
        tok.value = 'b'


# ---------------------------------------------------- tokenizer fallback paths
import re  # noqa: E402

from PyReprism.languages.base import BaseLanguage, _code_lexer  # noqa: E402


class _BackrefLang(BaseLanguage):
    """A long-bracket string ([==[...]==]) needs a backreference."""
    @classmethod
    def file_extension(cls):
        return '.zz1'

    @classmethod
    def comment_regex(cls):
        return re.compile(r'(?P<comment>--.*?$)|(?P<noncomment>.[^-]*)', re.DOTALL | re.MULTILINE)

    @classmethod
    def string_regex(cls):
        return re.compile(r'\[(=*)\[[\s\S]*?\]\1\]')


class _EmptyNumberLang(_BackrefLang):
    """A number pattern that can match the empty string."""
    @classmethod
    def file_extension(cls):
        return '.zz2'

    @classmethod
    def string_regex(cls):
        return re.compile(r'"[^"]*"')

    @classmethod
    def number_regex(cls):
        return re.compile(r'\d*')


def _typed(cls, src):
    return [(t.type, t.value, t.start, t.end, t.line) for t in cls.tokenize(src)]


def test_backreference_patterns_use_the_stage_loop():
    assert _code_lexer(_BackrefLang).combined is None
    src = 'x = [==[a]]b]==] -- c\ny'
    assert _typed(_BackrefLang, src) == [
        (TokenType.IDENTIFIER, 'x', 0, 1, 1), (TokenType.WHITESPACE, ' ', 1, 2, 1),
        (TokenType.OPERATOR, '=', 2, 3, 1), (TokenType.WHITESPACE, ' ', 3, 4, 1),
        (TokenType.STRING, '[==[a]]b]==]', 4, 16, 1), (TokenType.WHITESPACE, ' ', 16, 17, 1),
        (TokenType.COMMENT, '-- c', 17, 21, 1), (TokenType.WHITESPACE, '\n', 21, 22, 2),
        (TokenType.IDENTIFIER, 'y', 22, 23, 2)]


def test_empty_matches_fall_back_to_the_stage_loop():
    # At 'a' the number stage matches the empty string; the identifier stage
    # must win, exactly as in the stage-by-stage loop.
    assert _code_lexer(_EmptyNumberLang).combined is not None
    src = '12 ab\n"s" 3'
    assert _typed(_EmptyNumberLang, src) == [
        (TokenType.NUMBER, '12', 0, 2, 1), (TokenType.WHITESPACE, ' ', 2, 3, 1),
        (TokenType.IDENTIFIER, 'ab', 3, 5, 1), (TokenType.WHITESPACE, '\n', 5, 6, 2),
        (TokenType.STRING, '"s"', 6, 9, 2), (TokenType.WHITESPACE, ' ', 9, 10, 2),
        (TokenType.NUMBER, '3', 10, 11, 2)]


# ------------------------------------------- stats without building the tokens
from PyReprism import _tokenops  # noqa: E402

_STATS_SAMPLES = [
    'def f():\n    """Doc.\n\n    more"""\n    x = """a\n\nb"""  # c\n\n    return x\n',
    '/* a\n\n b */\nint main() { return "x//y" ? 1 : 0; } // c\n',
    '#!/bin/bash\n# c\necho "a # b" && ls\n\n',
    'local s = [[a\n-- b]] -- c\n',
]


@pytest.mark.parametrize('lang', ['python', 'c', 'bash', 'lua', 'odin', 'cobol'])
@pytest.mark.parametrize('src', _STATS_SAMPLES)
def test_counted_stats_equal_token_list_stats(lang, src):
    cls = pr_get(lang)
    assert cls.stats(src) == _tokenops.stats(cls.tokenize(src), src)


def test_counted_stats_fall_back_when_the_joined_pattern_is_not_usable():
    assert _BackrefLang._counted_stats('x = 1\n') is None          # no joined pattern
    assert _EmptyNumberLang._counted_stats('ab 1\n') is None       # empty match
    assert _EmptyNumberLang.stats('ab 1\n') == _tokenops.stats(
        _EmptyNumberLang.tokenize('ab 1\n'), 'ab 1\n')


def pr_get(lang):
    import PyReprism
    return PyReprism.get_language(lang)
