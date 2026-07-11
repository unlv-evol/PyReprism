.. _fingerprints_toplevel:

=========================================
Fingerprinting & similarity
=========================================

The :mod:`PyReprism.fingerprints` module detects clones and plagiarism using
**winnowing** k-gram fingerprints (Schleimer, Wilkerson & Aiken) over the
*normalized* token stream, so matches are robust to variable renaming and
literal changes (Type-2 clones)::

   from PyReprism import fingerprints as fp

   fp.similarity(code_a, code_b, "python")     # Jaccard of fingerprints, 0-1
   fp.containment(code_a, code_b, "python")    # fraction of A found in B

   index = fp.FingerprintIndex()
   index.add_paths("submissions/")
   index.similar_pairs(threshold=0.7)

Fingerprints are deterministic (CRC32-hashed) and comparable across runs.

.. automodule:: PyReprism.fingerprints
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
