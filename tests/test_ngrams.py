"""Tests for token n-gram analysis and the naturalness model."""
import io
import json

import pytest

from PyReprism import ngrams as ng
from PyReprism.ngrams import NgramModel, train
from PyReprism.languages import _load_all_languages
from PyReprism.languages.registry import LanguageRegistry
from PyReprism.cli import main

_load_all_languages()


# ---------------------------------------------------------------- extraction
def test_value_ngrams():
    grams = ng.ngrams('a = b + c', 'python', n=2)
    assert ('a', '=') in grams and ('+', 'c') in grams


def test_type_ngrams_are_structural():
    grams = ng.ngrams('a = 1', 'python', n=2, types=True)
    assert ('identifier', 'operator') in grams
    assert all(all(isinstance(t, str) for t in g) for g in grams)


def test_ngram_counts_and_padding():
    counts = ng.ngram_counts('a a a', 'python', n=2)
    assert counts[('a', 'a')] == 2
    padded = ng.ngrams('a', 'python', n=2, pad=True)
    assert ('<s>', 'a') in padded and ('a', '</s>') in padded


def test_comments_skipped_by_default():
    seq = ng.token_sequence('x = 1  # note', 'python')
    assert 'note' not in ' '.join(seq)
    seq2 = ng.token_sequence('x = 1  # note', 'python', include_comments=True)
    assert any('note' in t for t in seq2)


def test_ngrams_of_validates_n():
    with pytest.raises(ValueError):
        ng.ngrams_of(['a', 'b'], 0)


# --------------------------------------------------------------------- model
CORPUS = [
    'def f(x):\n    return x + 1\n',
    'def g(y):\n    return y * 2\n',
    'def h(z):\n    return z - 3\n',
]


def _model():
    return NgramModel(n=2).fit(ng.token_sequence(s, 'python') for s in CORPUS)


def test_natural_code_scores_lower_perplexity():
    m = _model()
    natural = ng.token_sequence('def k(w):\n    return w + 4\n', 'python')
    weird = ng.token_sequence('@ ~ ^ & | ? !', 'python')
    assert m.perplexity(natural) < m.perplexity(weird)


def test_perplexity_is_two_pow_cross_entropy():
    m = _model()
    seq = ng.token_sequence('def q(a):\n    return a + 7\n', 'python')
    assert m.perplexity(seq) == pytest.approx(2 ** m.cross_entropy(seq))


def test_model_persistence_round_trip():
    m = _model()
    restored = NgramModel.from_dict(json.loads(json.dumps(m.to_dict())))
    seq = ng.token_sequence(CORPUS[0], 'python')
    assert restored.perplexity(seq) == pytest.approx(m.perplexity(seq))


def test_model_rejects_bad_n():
    with pytest.raises(ValueError):
        NgramModel(n=0)


# ---------------------------------------------------------------------- train
def test_train_over_corpus(tmp_path):
    (tmp_path / 'a.py').write_text(CORPUS[0])
    (tmp_path / 'b.py').write_text(CORPUS[1])
    model = train(tmp_path, n=2)
    assert model.vocab
    assert model.perplexity(ng.token_sequence(CORPUS[0], 'python')) > 0


# ------------------------------------------------------ works for all languages
def test_token_sequence_for_all_languages():
    sample = 'a = f(x) + 1\n'
    for name, cls in LanguageRegistry.all().items():
        seq = ng.token_sequence(sample, cls)
        assert isinstance(seq, list)


# --------------------------------------------------------------------------- CLI
def test_cli_ngrams(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('a = b + c\na = b + d\n'))
    assert main(['ngrams', '--lang', 'python', '-n', '2', '--top', '3']) == 0
    out = capsys.readouterr().out
    assert 'a =' in out


def test_cli_ngrams_json(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('a = 1\n'))
    assert main(['ngrams', '--lang', 'python', '-n', '2', '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert isinstance(data, list) and isinstance(data[0][0], list)


def test_cli_perplexity(tmp_path, capsys):
    corpus = tmp_path / 'corpus'
    corpus.mkdir()
    for i, src in enumerate(CORPUS):
        (corpus / f'{i}.py').write_text(src)
    target = tmp_path / 'k.py'
    target.write_text('def k(w):\n    return w + 4\n')
    assert main(['perplexity', '--train', str(corpus), str(target)]) == 0
    out = capsys.readouterr().out
    assert str(target) in out
    assert float(out.split('\t')[0]) > 0
