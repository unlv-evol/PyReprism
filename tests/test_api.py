"""Tests for the high-level facade and the extract/count/match/tokenize API."""
import pytest

import PyReprism as pr
from PyReprism.languages import _load_all_languages
from PyReprism.languages.registry import LanguageRegistry
from PyReprism.tokens import Token, TokenType

_load_all_languages()
ALL_LANGUAGES = sorted(LanguageRegistry.all().items())

PY = '''# header
def add(a, b):
    n = 5 + 6      # inline
    s = "text 42"
    return a + b   # tail
'''


# --------------------------------------------------------------- facade routing
def test_get_language_by_name():
    assert pr.get_language('python').__name__ == 'Python'


def test_get_language_by_extension():
    assert pr.get_language('.go').__name__ == 'Go'


def test_get_language_by_class():
    cls = pr.get_language('python')
    assert pr.get_language(cls) is cls


def test_get_language_unknown_raises():
    with pytest.raises(ValueError):
        pr.get_language('not-a-language')


def test_detect_language_from_filename():
    assert pr.detect_language(filename='src/main.go').__name__ == 'Go'
    assert pr.detect_language(filename='unknown.zzz') is None


# ------------------------------------------------------------------- operations
def test_extract_and_count_comments():
    assert pr.extract_comments(PY, lang='python') == ['# header', '# inline', '# tail']
    assert pr.count_comments(PY, lang='python') == 3


def test_match_comments_positions():
    matches = pr.match_comments(PY, lang='python')
    assert all(isinstance(m, Token) and m.type is TokenType.COMMENT for m in matches)
    assert matches[0].value == '# header'
    assert matches[0].line == 1
    # spans round-trip back to the exact substring
    assert PY[matches[0].start:matches[0].end] == '# header'


def test_extract_numbers_and_keywords():
    assert pr.extract_numbers(PY, lang='python') == ['5', '6', '42']
    assert pr.extract_keywords(PY, lang='python') == ['def', 'return']


def test_extract_strings():
    assert pr.extract_strings(PY, lang='python') == ['"text 42"']


def test_remove_numbers():
    assert pr.remove_numbers('a = 5 + 60', lang='python') == 'a =  + '


def test_preprocess_pipeline():
    out = pr.preprocess(PY, lang='python', steps=['comments', 'whitespace'])
    assert '#' not in out
    assert 'def' in out


def test_preprocess_unknown_step():
    with pytest.raises(ValueError):
        pr.preprocess(PY, lang='python', steps=['bogus'])


def test_remove_whitespaces_language_independent():
    assert pr.remove_whitespaces('a  =\n\n b') == 'a=\nb'


# --------------------------------------------------------------------- tokenize
def test_tokenize_basic_classification():
    toks = pr.tokenize('x = 5 + y  // c\n', lang='clike')
    kinds = {t.type for t in toks}
    assert TokenType.IDENTIFIER in kinds
    assert TokenType.NUMBER in kinds
    assert TokenType.OPERATOR in kinds
    assert TokenType.COMMENT in kinds
    # every token round-trips to the original source
    src = 'x = 5 + y  // c\n'
    assert ''.join(t.value for t in toks) == src


def test_tokenize_keyword_vs_identifier():
    toks = pr.tokenize('def foo(): return 1', lang='python')
    by_val = {t.value: t.type for t in toks}
    assert by_val['def'] is TokenType.KEYWORD
    assert by_val['return'] is TokenType.KEYWORD
    assert by_val['foo'] is TokenType.IDENTIFIER


# --------------------------------------------------------- registry-wide safety
SAMPLE = 'value = 1 + 2 // c\n# h\nname = "x"\n'


@pytest.mark.parametrize('name, cls', ALL_LANGUAGES)
class TestEveryLanguageAPI:
    def test_extract_ops_return_lists(self, name, cls):
        assert isinstance(cls.extract_comments(SAMPLE), list)
        assert isinstance(cls.extract_numbers(SAMPLE), list)
        assert isinstance(cls.extract_strings(SAMPLE), list)
        assert isinstance(cls.extract_identifiers(SAMPLE), list)
        assert isinstance(cls.extract_keywords(SAMPLE), list)

    def test_count_ops_return_ints(self, name, cls):
        assert isinstance(cls.count_comments(SAMPLE), int)
        assert isinstance(cls.count_numbers(SAMPLE), int)

    def test_remove_ops_return_str(self, name, cls):
        assert isinstance(cls.remove_numbers(SAMPLE), str)
        assert isinstance(cls.remove_strings(SAMPLE), str)
        assert isinstance(cls.remove_operators(SAMPLE), str)

    def test_tokenize_covers_all_input(self, name, cls):
        toks = cls.tokenize(SAMPLE)
        # tokenizer must be lossless: concatenating token values rebuilds the input
        assert ''.join(t.value for t in toks) == SAMPLE
