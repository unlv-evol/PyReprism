"""Regressions found by comparing token classes with a tree-sitter oracle
(manuscript/scripts/experiments_token_oracle.py)."""
import pytest

import PyReprism as pr
from PyReprism.tokens import TokenType


def _kinds(source, lang, engine='regex'):
    return [(t.type, t.value) for t in pr.tokenize(source, lang=lang, engine=engine)
            if t.type in (TokenType.COMMENT, TokenType.STRING)]


def _squash(text):
    return ''.join(text.split())


@pytest.mark.parametrize('lang, source, expected', [
    # Text the comment regex skips must survive comment removal.
    ('c', '#include "api/z3.h" // c\nint x;\n', '#include "api/z3.h" \nint x;'),
    ('scala', 'object A { def f = 1 } // c\n', 'object A { def f = 1 }'),
    ('groovy', 'def u = "a/b" // c\n', 'def u = "a/b" '),
])
def test_remove_comments_keeps_all_code(lang, source, expected):
    assert _squash(pr.remove_comments(source, lang=lang)) == _squash(expected)


@pytest.mark.parametrize('lang', ['c', 'scala', 'css', 'python', 'javascript',
                                  'typescript', 'cpp', 'groovy', 'jsx', 'tsx'])
def test_remove_comments_matches_token_stream(lang):
    source = ('x = "a/b" /* c */ y // d\n# e\n"""f"""\nz = `g/h`\n'
              "w = '/' + u\n")
    kept = ''.join(t.value for t in pr.tokenize(source, lang=lang)
                   if t.type is not TokenType.COMMENT)
    assert _squash(pr.remove_comments(source, lang=lang)) == _squash(kept)


def test_css_strings_with_slashes_stay_whole():
    source = "a{src:url('../f/x.eot');/* c */}\nb{x:\"/*no*/\"}\n"
    assert _kinds(source, 'css') == [
        (TokenType.STRING, "'../f/x.eot'"), (TokenType.COMMENT, '/* c */'),
        (TokenType.STRING, '"/*no*/"')]


def test_python_triple_quoted_string_is_comment_only_at_line_start():
    source = ('def f():\n    """doc"""\n    x = """s # t"""\n'
              "    g(1, '''u''')\n")
    assert _kinds(source, 'python') == [
        (TokenType.COMMENT, '"""doc"""'), (TokenType.STRING, '"""s # t"""'),
        (TokenType.STRING, "'''u'''")]


@pytest.mark.parametrize('lang', ['javascript', 'typescript', 'jsx', 'tsx'])
def test_template_literals_are_strings(lang):
    source = 'const u = `http://x/${a}`; // c\n'
    assert _kinds(source, lang) == [(TokenType.STRING, '`http://x/${a}`'),
                                    (TokenType.COMMENT, '// c')]


@pytest.mark.parametrize('lang', ['c', 'cpp', 'java'])
def test_c_family_strings_containing_slashes_are_not_comments(lang):
    source = 'auto s = "http://x"; // c\nchar c = \'/\';\n'
    assert _kinds(source, lang) == [(TokenType.STRING, '"http://x"'),
                                     (TokenType.COMMENT, '// c'),
                                     (TokenType.STRING, "'/'")]


def test_pygments_preprocessor_directives_are_code():
    pytest.importorskip('pygments')
    source = '#include <stdio.h>\n#define X 1 /* c */\nint x;\n'
    kinds = _kinds(source, 'c', engine='pygments')
    assert (TokenType.COMMENT, '/* c */') in kinds
    assert all('#include' not in v and '#define' not in v
               for t, v in kinds if t is TokenType.COMMENT)
    assert pr.stats(source, lang='c', engine='pygments').comment_lines == 0


@pytest.mark.parametrize('lang', ['javascript', 'typescript', 'jsx', 'tsx'])
@pytest.mark.parametrize('source, comment', [
    ('var r = /^\\/\\//, s = x / y / z; // c\n', '// c'),
    ('if (/\\/\\*/.test(a)) b = 1; /* k */\n', '/* k */'),
    ('a = b/2; // d\n', '// d'),
])
def test_regex_literals_do_not_start_comments(lang, source, comment):
    assert [v for t, v in _kinds(source, lang) if t is TokenType.COMMENT] == [comment]


def test_pygments_docstrings_follow_the_regex_engine_policy():
    pytest.importorskip('pygments')
    source = 'def f():\n    """doc"""\n    x = "s"\n'
    assert _kinds(source, 'python', engine='pygments') == _kinds(source, 'python')


# Languages where the probe is not meaningful: '"' starts a comment (Abap,
# SmallTalk, Vim), every character has a meaning (BrainFuck), comments are
# column-based (Cobol), '"' is not a string delimiter (Pascal), or '#' starts a
# comment even inside quotes (MakeFile).
_PROBE_EXEMPT = {'Abap', 'SmallTalk', 'Vim', 'BrainFuck', 'Cobol', 'Pascal', 'MakeFile'}


def _all_languages():
    from PyReprism.languages import _load_all_languages
    from PyReprism.languages.registry import LanguageRegistry
    _load_all_languages()
    return sorted(LanguageRegistry.all().items())


@pytest.mark.parametrize('name, cls', [(n, c) for n, c in _all_languages()
                                       if n not in _PROBE_EXEMPT])
def test_double_quoted_strings_with_comment_delimiters_stay_whole(name, cls):
    probe = 'x = "p/q//r#s;t--u" + y\n'
    tokens = cls.tokenize(probe)
    assert ''.join(t.value for t in tokens) == probe
    assert not [t for t in tokens if t.type is TokenType.COMMENT], name


@pytest.mark.parametrize('lang, source, comments', [
    ('lua', 'a = [[x -- y]] -- c\n--[==[ k ]==]\n', ['-- c', '--[==[ k ]==]']),
    ('yaml', 'url: http://x/#frag # c\nq: "a # b"\n', ['# c']),
    ('tcl', 'puts #notacomment ;# c\n# d\n', ['# c', '# d']),
    ('docker', 'RUN echo "#x"\n# c\n', ['# c']),
    ('properties', 'k = v#1\n! c\n', ['! c']),
    ('scheme', '(display #\\;) ; c\n', ['; c']),
    ('elixir', 'x = ?# # c\n', ['# c']),
    ('erb', '<a href="#top"><%# c %></a>\n', ['<%# c %>']),
    ('scss', 'a { b: url(http://x/y.png); } // c\n', ['// c']),
    ('ada', "X'First -- c\nS := \"a--b\";\n", ['-- c']),
    ('sql', "select '--x', 'a/*b' -- c\n", ['-- c']),
    ('less', "@u: 'http://x'; // c\n", ['// c']),
])
def test_language_specific_comment_rules(lang, source, comments):
    found = [t.value.strip() for t in pr.tokenize(source, lang=lang)
             if t.type is TokenType.COMMENT]
    assert found == comments


# Defects found on the project-stratified evaluation sample.
def test_go_raw_strings_keep_comment_markers():
    source = 's := `a // b /* c */` // d\n'
    assert _kinds(source, 'go') == [(TokenType.STRING, '`a // b /* c */`'),
                                    (TokenType.COMMENT, '// d')]


@pytest.mark.parametrize('source', ['echo $# ${#a} a#b\n', 'n=${#list[@]}\n'])
def test_bash_hash_inside_a_word_is_not_a_comment(source):
    assert not [v for t, v in _kinds(source, 'bash') if t is TokenType.COMMENT]


def test_bash_comments_start_at_word_boundaries():
    found = [v for t, v in _kinds('x=1 # a\n# b\ny=2;# c\n', 'bash') if t is TokenType.COMMENT]
    assert found == ['# a', '# b', '# c']


@pytest.mark.parametrize('engine', ['regex', 'pygments'])
def test_byte_order_mark_is_whitespace(engine):
    if engine == 'pygments':
        pytest.importorskip('pygments')
    source = '﻿// licence\nint x;\n'
    stats = pr.stats(source, lang='csharp', engine=engine)
    assert (stats.comment_lines, stats.code_lines) == (1, 1)


def test_python_strings_passed_as_arguments_are_not_docstrings():
    source = ('def f():\n    """Doc."""\n    g(\n        """arg"""\n    )\n'
              '    h(a,\n      """two""")\n    y = (\n    """v""")\n"""mod"""\n')
    assert _kinds(source, 'python') == [
        (TokenType.COMMENT, '"""Doc."""'), (TokenType.STRING, '"""arg"""'),
        (TokenType.STRING, '"""two"""'), (TokenType.STRING, '"""v"""'),
        (TokenType.COMMENT, '"""mod"""')]


def test_python_operators_stay_whole_near_argument_strings():
    source = 'if key == ID and a != b:\n    f(x,\n      """s""")\n'
    ops = [t.value for t in pr.tokenize(source, lang='python')
           if t.type is TokenType.OPERATOR]
    assert '==' in ops and '!=' in ops
