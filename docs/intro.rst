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
**lexical** tier (default), an optional **syntactic** tier (`tree-sitter ASTs
<https://pyreprism.readthedocs.io/en/latest/syntactic.html>`__ for precise per-function metrics),
and an optional **semantic** tier (`code embeddings
<https://pyreprism.readthedocs.io/en/latest/semantic.html>`__ for Type-4 clone detection).

Highlights
==========

* One consistent API for every language: ``remove_*`` / ``extract_*`` /
  ``count_*`` / ``match_*`` for each construct, plus a lossless ``tokenize()``.
* Code metrics (``stats``) and ML canonicalization (``normalize``) for
  clone/plagiarism detection and code-embedding pipelines.
* Optional high-accuracy `Pygments`_ backend and an on-demand Pygments fallback
  for 500+ languages — with **zero required dependencies** by default.
* Optional `syntactic (AST) <https://pyreprism.readthedocs.io/en/latest/syntactic.html>`__ and
  `semantic (embedding) <https://pyreprism.readthedocs.io/en/latest/semantic.html>`__ tiers for
  precise per-function metrics and Type-4 clone detection.
* Located clone detection with console, JSON, SARIF, Markdown, and HTML
  reports and a duplication gate for CI (also as a GitHub Action).
* Batch/corpus analysis on every core, and unified/``git`` diff processing.
* A ``pyreprism`` command-line tool (also ``python -m PyReprism``).

Stability
=========

PyReprism 1.0 is the first stable release. From 1.0 on, releases follow
`semantic versioning`_: the public API and the ``pyreprism`` command line change
incompatibly only in a new major version. Modules whose names start with an
underscore are internal. Token classifications may still change in minor
releases when they fix a lexer defect; the changelog lists every such change.

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
    pyreprism clones src/ --max-duplication 5   # located clones; fail above 5%

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
.. _semantic versioning: https://semver.org
