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

Options
=======

- ``-l, --lang`` — language name, extension, or class.
- ``-e, --engine`` — ``regex`` (default), ``pygments``, or ``auto``.
- ``-o, --output DIR`` — write results into ``DIR``, mirroring the input tree.
- ``-i, --in-place`` — rewrite files in place.
- ``--json`` / ``--csv`` — machine-readable output where supported.

Run ``pyreprism --help`` or ``pyreprism <command> --help`` for the full list.
