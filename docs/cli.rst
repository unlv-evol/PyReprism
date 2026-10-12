.. _cli_toplevel:

======================
Command-line interface
======================

Installing PyReprism provides a ``pyreprism`` command (equivalently
``python -m PyReprism``). It reads from stdin, files, globs, or directories, and
auto-detects the language from a file's extension (or a ``#!`` shebang on stdin)
when ``--lang`` is omitted.

Common usage
============

.. code-block:: shell

   pyreprism remove comments file.py
   cat file.go | pyreprism remove comments --lang go
   pyreprism extract comments "src/**/*.py" --json
   pyreprism count comments file.py --lang python
   pyreprism preprocess --steps comments,strings,whitespace file.java
   pyreprism tokenize --json file.py
   pyreprism normalize file.py
   pyreprism stats --json file.py

Directories and reports
=======================

.. code-block:: shell

   pyreprism scan myproject/ --csv              # aggregate metrics over a tree
   pyreprism scan myproject/ --json --per-file
   pyreprism remove comments src/ --output out/ # bulk-transform, mirroring the tree
   pyreprism remove comments file.py --in-place
   pyreprism scan myproject/ -j 1               # one process (default: one per CPU)

Analysis commands
=================

.. code-block:: shell

   pyreprism stats --full file.py                # add complexity metrics
   git diff | pyreprism diff --per-file          # churn split into code/comment/blank
   git diff | pyreprism diff --cosmetic          # comment/whitespace-only changes
   pyreprism similarity a.py b.py                # fingerprint similarity (0-1)
   pyreprism clones src/ --near --reporter sarif --max-duplication 5
   pyreprism ngrams file.py -n 3 --top 20
   pyreprism perplexity --train corpus/ file.py
   pyreprism languages                           # built-in languages and extensions
   pyreprism languages --pygments                # the Pygments fallback tier

``pyreprism clones`` exits with a non-zero status when ``--max-duplication`` is
exceeded, so it can gate continuous integration; see :doc:`clones`.

Options
=======

- ``-l, --lang`` — language name, extension, or class.
- ``-e, --engine`` — ``regex`` (default), ``pygments``, or ``auto``.
- ``-o, --output DIR`` — write results into ``DIR``, mirroring the input tree.
- ``-i, --in-place`` — rewrite files in place.
- ``--json`` / ``--csv`` — machine-readable output where supported.
- ``-j, --jobs N`` — ``scan`` and ``clones``: number of processes (default 0, one per CPU).
- ``--version`` — print the installed version.

Run ``pyreprism --help`` or ``pyreprism <command> --help`` for the full list.
