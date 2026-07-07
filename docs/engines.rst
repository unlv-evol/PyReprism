.. _engines_toplevel:

============
Engines
============

PyReprism can tokenize with different backends. The default ``regex`` engine is
zero-dependency; the optional ``pygments`` engine (``pip install
pyreprism[accurate]``) is more accurate — for example it will not treat a ``#``
inside a string as a comment. Select one per call with ``engine=``.

.. automodule:: PyReprism.engines
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__

.. automodule:: PyReprism.engines.base
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
