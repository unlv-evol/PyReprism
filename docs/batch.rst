.. _batch_toplevel:

============================
Batch / directory processing
============================

The :mod:`PyReprism.batch` module analyzes or transforms whole source trees.
Discovery skips junk folders (``.git``, ``node_modules``, ``venv``, …) and files
with unrecognized extensions::

   from PyReprism import batch

   report = batch.analyze("myproject/")
   report.totals()
   report.by_language()
   print(report.to_csv())

   batch.transform("myproject/",
                   lambda text, lang: lang.remove_comments(text),
                   output="stripped/")

Parallel processing
===================

Files are independent, so ``analyze``, ``transform``, ``map_files``, and
:func:`PyReprism.clones.detect` can use every core: pass ``jobs=0`` for one
process per CPU, or ``jobs=N``. The default, ``jobs=1``, runs in the calling
process. Results are identical for any number of jobs. With ``jobs`` other
than 1, functions you pass must be picklable (defined at module level, not
lambdas)::

   def metrics_and_copy(text, lang):            # any per-file analysis
       return lang.code_metrics(text), lang.normalize(text)

   for path, lang, (metrics, normalized) in batch.map_files(
           "myproject/", metrics_and_copy, jobs=0):
       ...

Besides each language's primary extension, discovery recognizes common
secondary ones, e.g. ``.h`` (C), ``.cc``/``.hpp`` (C++), ``.mjs``/``.cjs``,
``.pyi``, ``.bash``/``.zsh``, and ``.yml``.

.. automodule:: PyReprism.batch
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
