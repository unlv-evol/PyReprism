.. _tokens_toplevel:

===========
Tokens
===========

:meth:`~PyReprism.languages.base.BaseLanguage.tokenize` returns a flat, lossless
list of :class:`~PyReprism.tokens.Token` objects; concatenating every token's
``value`` reproduces the original source exactly.

.. automodule:: PyReprism.tokens
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
