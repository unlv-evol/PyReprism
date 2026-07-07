.. _api_toplevel:

================
High-level API
================

The top-level :mod:`PyReprism` package exposes a convenience API. Import it as
``pr`` and pass ``lang`` as a language name (``"python"``), a file extension
(``".py"``), or a language class::

   import PyReprism as pr

   pr.remove_comments(source, lang="python")
   pr.extract_comments(source, lang="python")
   pr.count_comments(source, lang="python")
   pr.tokenize(source, lang="python")
   pr.normalize(source, lang="python")
   pr.stats(source, lang="python")
   pr.preprocess(source, lang="java", steps=["comments", "strings", "whitespace"])

Every operation accepts ``engine="regex"`` (default), ``engine="pygments"``
(requires ``pip install pyreprism[accurate]``), or ``engine="auto"``.

The re-exported ``Token``, ``TokenType``, ``CodeStats`` and ``Normalizer`` are
documented on their own pages (:doc:`tokens`, :doc:`metrics`, :doc:`normalizer`).

.. automodule:: PyReprism
   :members:
   :undoc-members:
   :exclude-members: __dict__, __weakref__, Token, TokenType, CodeStats, Normalizer
