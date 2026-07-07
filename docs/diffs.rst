.. _diffs_toplevel:

===============
Diff processing
===============

The :mod:`PyReprism.diffs` module parses unified/``git`` diffs and analyzes the
changed code in each file's own language. It powers churn metrics (added/removed
lines split into code, comment and blank), cosmetic-change detection, and
ML-oriented extraction of the changed code::

   from PyReprism import diffs

   d = diffs.parse(diff_text)
   report = diffs.diff_stats(d)
   report.totals()
   diffs.cosmetic_files(d)

   f = d.files[0]
   f.added_text()
   f.normalize("added")

By default analysis is *fragment mode* (from the diff text alone). Setting a
:class:`~PyReprism.diffs.DiffFile`'s ``new_source`` / ``old_source`` to the full
file contents switches it to accurate *full-file mode* for that file.

.. automodule:: PyReprism.diffs
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
