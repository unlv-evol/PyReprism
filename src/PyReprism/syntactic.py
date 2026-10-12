"""Syntactic tier: tree-sitter ASTs for precise, structure-aware analysis.

This is the middle-high rung of PyReprism's analysis ladder. The default lexical
engine approximates cyclomatic complexity by counting decision *tokens*, which is
cheap and broad but degrades where control flow is not keyword-shaped (see the
accuracy/cost study). When precision matters, this tier parses a real AST with
tree-sitter and counts decision *nodes*, and it can extract function/method
boundaries for per-unit metrics.

It is optional: ``pip install pyreprism[ast]`` (``tree-sitter-language-pack``).
Import always succeeds; :func:`available` reports readiness and calls degrade
gracefully, so the zero-dependency lexical core is untouched.
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

# PyReprism/Pygments language name -> tree-sitter-language-pack name.
_TS_NAME = {
    "python": "python", "java": "java", "javascript": "javascript",
    "typescript": "typescript", "go": "go", "c": "c", "cpp": "cpp",
    "c++": "cpp", "csharp": "csharp", "c#": "csharp", "ruby": "ruby",
    "rust": "rust", "php": "php", "scala": "scala", "kotlin": "kotlin",
    "swift": "swift", "bash": "bash",
}

# Node types that introduce a decision point (+1 to cyclomatic complexity),
# unioned across the common tree-sitter grammars.
_DECISION_NODES = frozenset({
    "if_statement", "elif_clause", "else_if_clause",
    "for_statement", "for_in_statement", "for_range_loop",
    "enhanced_for_statement", "foreach_statement", "range_clause",
    "while_statement", "do_statement",
    "case", "case_statement", "switch_label", "when_entry", "when_clause",
    "expression_case", "type_case", "communication_case", "default_case",
    "catch_clause", "except_clause", "rescue_clause", "rescue",
    "conditional_expression", "ternary_expression",
})

# Logical operators that add a decision point.
_DECISION_OPS = frozenset({"&&", "||", "and", "or"})

# Node types that are functions/methods (for per-unit extraction).
_FUNCTION_NODES = frozenset({
    "function_definition", "function_declaration", "function_item",
    "method_declaration", "method_definition", "method", "constructor_declaration",
    "func_literal", "lambda", "arrow_function",
})


def available() -> bool:
    """True if tree-sitter grammars can be loaded."""
    try:
        import tree_sitter_language_pack  # noqa: F401
        return True
    except ImportError:
        return False


def _ts_name(lang: str) -> Optional[str]:
    return _TS_NAME.get((lang or "").lower())


@lru_cache(maxsize=64)
def _parser(ts_name: str):
    from tree_sitter_language_pack import get_parser
    return get_parser(ts_name)


def supported(lang: str) -> bool:
    """True if this tier can parse ``lang`` (grammar present and mapped)."""
    name = _ts_name(lang)
    if name is None or not available():
        return False
    try:
        _parser(name)
        return True
    except Exception:
        return False


def parse(code: str, lang: str):
    """Return the tree-sitter ``Tree`` for ``code`` in ``lang``.

    Raises ``ImportError`` if grammars are unavailable or ``ValueError`` if the
    language is unsupported---callers can fall back to the lexical tier.
    """
    if not available():
        raise ImportError("the syntactic tier requires tree-sitter-language-pack; "
                          "install with `pip install pyreprism[ast]`.")
    name = _ts_name(lang)
    if name is None:
        raise ValueError(f"no tree-sitter mapping for language {lang!r}")
    return _parser(name).parse(code.encode("utf-8", "replace"))


def _walk(node):
    stack = [node]
    while stack:
        n = stack.pop()
        yield n
        stack.extend(n.children)


def cyclomatic(code: str, lang: str) -> int:
    """Precise McCabe cyclomatic complexity via decision *nodes*: ``1 + decisions``.

    Counts control-flow nodes and short-circuit logical operators in the AST.
    """
    tree = parse(code, lang)
    decisions = 0
    for node in _walk(tree.root_node):
        if node.type in _DECISION_NODES:
            decisions += 1
        elif node.type in ("binary_expression", "boolean_operator",
                           "logical_expression", "binary_operator"):
            op = node.child_by_field_name("operator")
            if op is not None and op.type in _DECISION_OPS:
                decisions += 1
    return decisions + 1


@dataclass
class FunctionInfo:
    name: str
    start_byte: int
    end_byte: int
    start_line: int
    cyclomatic: int


def _node_name(node) -> str:
    ident = node.child_by_field_name("name")
    if ident is not None:
        return ident.text.decode("utf-8", "replace")
    for ch in node.children:
        if ch.type in ("identifier", "field_identifier", "property_identifier"):
            return ch.text.decode("utf-8", "replace")
    return "<anonymous>"


def functions(code: str, lang: str) -> List[FunctionInfo]:
    """Extract functions/methods with per-unit cyclomatic complexity."""
    tree = parse(code, lang)
    out: List[FunctionInfo] = []
    for node in _walk(tree.root_node):
        if node.type in _FUNCTION_NODES:
            decisions = 0
            for inner in _walk(node):
                if inner is node:
                    continue
                if inner.type in _DECISION_NODES:
                    decisions += 1
                elif inner.type in ("binary_expression", "boolean_operator",
                                    "logical_expression", "binary_operator"):
                    op = inner.child_by_field_name("operator")
                    if op is not None and op.type in _DECISION_OPS:
                        decisions += 1
            out.append(FunctionInfo(
                name=_node_name(node),
                start_byte=node.start_byte, end_byte=node.end_byte,
                start_line=node.start_point[0] + 1, cyclomatic=decisions + 1))
    return out
