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

.. automodule:: PyReprism.batch
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
