# Changelog

All notable changes to PyReprism are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Complexity metrics** computed from the token stream: `halstead()`
  (volume/difficulty/effort/bugs), `cyclomatic_complexity()` (approximate McCabe),
  `maintainability_index()` (0–100), `max_nesting_depth()`, and `code_metrics()`
  which bundles them with the line/token stats. Exposed on the CLI via
  `pyreprism stats --full`.
- **Diff processing** (`PyReprism.diffs`): parse unified/`git` diffs and analyze
  the changed code per file in its own language. Includes churn metrics
  (`diff_stats`: added/removed split into code, comment and blank), cosmetic
  (comment/whitespace-only) change detection, reconstruction of the added/removed
  code, and ML-oriented `tokenize`/`normalize`/`extract_comments` on changes.
  Fragment mode works from the diff alone; setting a file's `new_source` /
  `old_source` enables accurate full-file classification. New CLI command
  `pyreprism diff` (`--json` / `--csv` / `--per-file` / `--cosmetic`).

## [0.1.0] - 2026-07-07

This release turns PyReprism from a comment-removal helper into a full
source-preprocessing toolkit with a high-level API, a CLI, code metrics,
ML-oriented normalization, an optional accurate backend, and batch processing.

### Added
- **High-level API** (`import PyReprism as pr`): `remove_*`, `extract_*`,
  `count_*`, `match_*` for comments, keywords, numbers, operators, strings and
  identifiers; plus `preprocess`, `remove_whitespaces`, `get_language` and
  `detect_language`. `lang=` accepts a language name, file extension, or class.
- **Tokenizer**: `tokenize()` on every language returns a lossless, typed
  `Token` stream (`Token`/`TokenType` in `PyReprism.tokens`).
- **Code metrics**: `stats()` returns a `CodeStats` (line/token counts,
  comment-to-code ratio, comment density; `as_dict()` for JSON/dataframes).
- **ML normalization**: `normalize()` canonicalizes code (rename identifiers to
  `VAR1…`, mask string/number literals, drop comments) for clone/plagiarism
  detection and code-embedding pipelines; `blank_comments()` strips comments
  while preserving line numbers.
- **Pluggable backends**: `engine="regex"` (default, zero-dependency) or
  `engine="pygments"` (`pip install pyreprism[accurate]`) for higher accuracy,
  plus `"auto"`. Available on every operation.
- **Batch processing** (`PyReprism.batch`): `analyze()` walks a directory tree
  and returns an aggregate report (`to_json`/`to_csv`, per-language breakdown);
  `transform()` bulk-applies a transformation into a mirrored output directory.
- **Command-line interface** (`pyreprism`, also `python -m PyReprism`):
  `remove`, `extract`, `count`, `preprocess`, `tokenize`, `stats`, `normalize`,
  `scan`, and `languages`; reads stdin/files/globs/directories; supports
  `--lang`, `--engine`, `--in-place`, `--output`, and `--json`/`--csv`.
- **Source-based language detection**: `detect_language(source=...)` recognizes
  `#!` shebangs and (when Pygments is installed) makes a best-effort content
  guess; the CLI uses this to auto-detect the language of piped input.
- Pre-commit hooks (`.pre-commit-hooks.yaml`), a `py.typed` marker (PEP 561),
  and a registry-wide test suite covering all supported languages.

### Changed
- Implemented real support for 25 previously-empty language stubs and migrated
  22 legacy languages (HTML, JSON, YAML, CSS, Markdown, …) to the
  `BaseLanguage` + registry pattern, making them importable via the public API.
- Ambiguous file extensions now resolve to a canonical language
  (`.py` → Python, `.js` → JavaScript, …).
- Consolidated packaging into `pyproject.toml` (single version source, pytest
  and coverage config), updated CI to a Python 3.8–3.12 matrix, and refreshed
  the README.

### Fixed
- Corrected comment-stripping for ~30 languages whose regexes either failed to
  remove line comments or consumed surrounding code, and fixed duplicate/broken
  definitions (Perl, csp, glsl, django, apacheconf, php_extras, ruby, and the
  Python triple-quoted-docstring bug).

## [0.0.4] - 2024

- Early beta releases: comment removal for an initial set of languages and the
  `Normalizer` whitespace helper.

[Unreleased]: https://github.com/unlv-evol/PyReprism/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/unlv-evol/PyReprism/releases/tag/v0.1.0
[0.0.4]: https://github.com/unlv-evol/PyReprism/releases/tag/v0.0.4
