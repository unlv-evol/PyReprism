.. _syntactic_toplevel:

=========================================
Syntactic tier (tree-sitter ASTs)
=========================================

The :mod:`PyReprism.syntactic` module is the *optional* middle rung of the
fidelity ladder. Where the lexical tier approximates cyclomatic complexity by
counting decision *tokens*, this tier parses a real `tree-sitter`_ AST and counts
decision *nodes*, giving exact and — crucially — **per-function** metrics that a
token stream cannot provide.

Install the extra::

   pip install "PyReprism[ast]"

Usage::

   from PyReprism import syntactic as ast

   ast.available()                 # True if tree-sitter grammars are installed
   ast.supported("java")           # True if this language can be parsed

   ast.cyclomatic(src, "java")     # precise McCabe complexity (1 + decision nodes)
   ast.functions(src, "python")    # -> [FunctionInfo(name, start_line, cyclomatic), ...]
   tree = ast.parse(src, "go")     # the raw tree-sitter Tree

The tier degrades gracefully: when the extra is not installed, :func:`available`
returns ``False`` and callers can fall back to the lexical tier. At the file
level the token approximation is already competitive with the AST; the AST's
distinctive value is *granularity* (per-function decomposition) and exactness on
control flow that is not keyword-shaped. See ``manuscript/`` for a measured
comparison against `lizard`_.

.. _tree-sitter: https://tree-sitter.github.io/
.. _lizard: https://github.com/terryyin/lizard

.. automodule:: PyReprism.syntactic
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __dict__, __weakref__
