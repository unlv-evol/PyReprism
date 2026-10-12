.. _intro_toplevel:

========
Overview
========

**PyReprism** is a Python framework for source-code preprocessing. It lets you
**match, extract, count, and remove** comments, strings, numbers, operators,
keywords and other language-specific constructs across **187+ programming
languages and file formats** (500+ with the optional Pygments backend) — through a
small high-level API, a command-line tool, code metrics, ML-oriented
normalization, and diff/pull-request analysis.

Everything is derived from one lossless token stream, and the same substrate
anchors a **fidelity ladder** of optional-cost tiers: a zero-dependency
**lexical** tier (default), an optional **syntactic** tier (:doc:`tree-sitter
ASTs <syntactic>` for precise per-function metrics), and an optional **semantic**
tier (:doc:`code embeddings <semantic>` for Type-4 clone detection).

Highlights
==========

* One consistent API for every language: ``remove_*`` / ``extract_*`` /
  ``count_*`` / ``match_*`` for each construct, plus a lossless ``tokenize()``.
* Code metrics (``stats``) and ML canonicalization (``normalize``) for
  clone/plagiarism detection and code-embedding pipelines.
* Optional high-accuracy `Pygments`_ backend and an on-demand Pygments fallback
  for 500+ languages — with **zero required dependencies** by default.
* Optional :doc:`syntactic (AST) <syntactic>` and :doc:`semantic (embedding)
  <semantic>` tiers for precise per-function metrics and Type-4 clone detection.
* Batch/corpus analysis and unified/``git`` diff processing.
* A ``pyreprism`` command-line tool (also ``python -m PyReprism``).

Requirements
============

* `Python`_ 3.8 or newer

Install
=======

.. code-block:: shell

    pip install PyReprism

The optional tiers are opt-in extras (install only what you need):

.. code-block:: shell

    pip install "PyReprism[accurate]"    # Pygments backend (higher lexical fidelity)
    pip install "PyReprism[ast]"         # syntactic tier (tree-sitter)
    pip install "PyReprism[semantic]"    # semantic tier (code embeddings)

Quick start
===========

.. code-block:: python

    import PyReprism as pr

    source = """
    # a comment
    x = 5 + 6
    print(x)  # inline
    """

    pr.remove_comments(source, lang="python")   # code without comments
    pr.extract_comments(source, lang="python")  # ['# a comment', '# inline']
    pr.count_comments(source, lang="python")     # 2

``lang`` accepts a language name (``"python"``), a file extension (``".py"``),
or a language class. Canonicalize code for machine learning, or measure it:

.. code-block:: python

    pr.normalize("total = price * 42", lang="python")   # 'VAR1 = VAR2 * 0'
    pr.stats(source, lang="python").comment_to_code_ratio

Command line
============

.. code-block:: shell

    pyreprism remove comments file.py
    pyreprism scan myproject/ --csv          # aggregate code metrics over a tree
    git diff | pyreprism diff --cosmetic     # flag comment/whitespace-only changes

Documentation
=============

Full documentation, including the API reference and the list of supported
languages, is available at https://pyreprism.readthedocs.io.

Source code
===========

PyReprism is developed on GitHub at
https://github.com/unlv-evol/PyReprism. To work on it locally:

.. code-block:: shell

    git clone https://github.com/unlv-evol/PyReprism.git
    cd PyReprism
    python3 -m venv venv && source venv/bin/activate
    pip install -e ".[dev]"
    pytest

See ``CONTRIBUTING.md`` for contribution guidelines.

.. _Python: https://www.python.org
.. _Pygments: https://pygments.org
