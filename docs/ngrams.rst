.. _ngrams_toplevel:

==============================
N-grams & code naturalness
==============================

The :mod:`PyReprism.ngrams` module extracts token n-grams and provides an
n-gram language model for measuring code *naturalness* (cross-entropy /
perplexity), following Hindle et al., "On the Naturalness of Software".

n-grams can be taken over token **text** or over token **types** (structural,
AST-free), which is useful for clone detection and style analysis::

   from PyReprism import ngrams

   ngrams.ngram_counts(source, "python", n=3).most_common(10)
   ngrams.ngrams(source, "python", n=2, types=True)

   model = ngrams.train("corpus/", n=3)
   seq = ngrams.token_sequence(source, "python")
   model.perplexity(seq)      # lower = more predictable / "natural"
   model.save("model.json")

.. automodule:: PyReprism.ngrams
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
