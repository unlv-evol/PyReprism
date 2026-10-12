.. _clones_toplevel:

=========================================
Located clones & reports
=========================================

The :mod:`PyReprism.clones` module complements :doc:`fingerprints <fingerprints>`
(which return a file-level *similarity score*) with **located fragments** — which
line ranges are duplicated between files — found by a Rabin-Karp scan over the
normalized token stream. It also produces a **unified report** spanning all three
rungs of the fidelity ladder, each clone tagged with a ``kind``:

* ``exact``    — Type-1/2 located fragments (rename-invariant when normalized);
* ``near``     — Type-3 file-level near-duplicates (winnowing fingerprints);
* ``semantic`` — Type-4 clones (:doc:`code embeddings <semantic>`), at function
  granularity when the :doc:`syntactic tier <syntactic>` is available.

::

   from PyReprism import clones, reporters

   report = clones.detect("src/", min_tokens=50, min_lines=5,
                          near=True, semantic=True)
   report.duplication_pct                 # % duplicated lines
   for c in report.clones:
       print(c.kind, c.a.path, c.a.start_line, c.b.path, c.b.start_line)

Every clone — including **semantic (Type-4)** ones — flows through the same
reporters, so CI can surface lexical and semantic duplication uniformly::

   reporters.to_sarif(report)      # GitHub code scanning (rule id per kind)
   reporters.to_markdown(report)   # PR comment
   reporters.to_json(report)
   reporters.to_html(report)       # self-contained, theme-aware HTML page

The **HTML reporter** renders a self-contained page (no external assets beyond
web fonts): a duplication meter with an optional ``max_duplication`` CI-gate
marker, per-kind counts, and one filterable card per clone showing its located
line ranges, score, and SARIF rule id. Exact and function-level clones also get
a side-by-side source snippet with the duplicated range highlighted (read from
disk; missing files are skipped)::

   html = reporters.to_html(report, target="src/", max_duplication=5)
   open("clones.html", "w").write(html)

On the command line, ``pyreprism clones`` exposes ``--min-tokens`` / ``--min-lines``,
``--near`` / ``--semantic``, ``--reporter {console,json,sarif,markdown,html}``, and a
``--max-duplication PCT`` CI gate (non-zero exit above the threshold). It uses one
process per CPU by default (``-j 1`` for one process; ``jobs=`` in
``clones.detect``), with identical results::

   pyreprism clones src/ --near --reporter html --max-duplication 5 > clones.html

.. automodule:: PyReprism.clones
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__

Reporters
=========

.. automodule:: PyReprism.reporters
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
