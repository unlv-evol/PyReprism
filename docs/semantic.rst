.. _semantic_toplevel:

=========================================
Semantic tier (code embeddings)
=========================================

The :mod:`PyReprism.semantic` module is the *optional* highest rung of the
fidelity ladder and the only one that is not lexical. Winnowing
:doc:`fingerprints <fingerprints>` detect Type-1/2/3 clones but, by construction,
cannot detect **Type-4** clones (semantically equivalent, syntactically
different). This tier embeds code with a code-search transformer and ranks by
cosine similarity, mirroring the :class:`~PyReprism.fingerprints.FingerprintIndex`
API.

Install the extra::

   pip install "PyReprism[semantic]"

Usage::

   from PyReprism import semantic

   semantic.available()                       # True if transformers+torch present
   semantic.similarity(code_a, code_b)        # cosine similarity in embedding space

   idx = semantic.EmbeddingIndex()
   idx.add_paths("submissions/")
   idx.similar_pairs(threshold=0.8)           # semantic near-duplicate pairs
   idx.query(code, k=5)                        # k most similar indexed snippets

The tier degrades gracefully: when the extra is not installed, :func:`available`
returns ``False`` and the zero-dependency lexical core is unaffected. The
embedding tier recovers Type-4 clones that lexical methods miss, but it is *not* a
strict superset — synthetic identifier renaming, which token normalization handles
exactly, can degrade it. Use the lexical tier for Type-1/2/3 screening and the
semantic tier for Type-4; see ``manuscript/`` for a measured account.

.. automodule:: PyReprism.semantic
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
