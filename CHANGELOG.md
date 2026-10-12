# Changelog

All notable changes to PyReprism are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-12

The first stable release. The public API (the top-level functions, the
language classes, `Token`/`TokenType`, `CodeStats`, and the `batch`, `diffs`,
`fingerprints`, `ngrams`, `clones`, `reporters`, `syntactic`, and `semantic`
modules) and the `pyreprism` command line now follow semantic versioning:
breaking changes only in a new major version. This release adds located clone
detection with CI reports, optional syntactic and semantic tiers, and parallel
processing; makes tokenization several times faster; and fixes the lexer
defects found by validating token classes against tree-sitter parses on a
project-stratified sample of open-source code.

### Added
- **Located clones and reports** (`PyReprism.clones`, `PyReprism.reporters`):
  `clones.detect()` finds which line ranges are duplicated between files
  (Rabin-Karp over the normalized token stream, with jscpd-style
  `min_tokens`/`min_lines` floors), optionally adds Type-3 near-duplicate files
  (`near=True`) and Type-4 semantic clones (`semantic=True`), and reports the
  percentage of duplicated lines. Reporters render console, JSON, SARIF (one
  rule id per clone kind), Markdown, and a self-contained HTML page. CLI:
  `pyreprism clones --reporter ... --max-duplication PCT` (non-zero exit above
  the threshold, for CI).
- **Syntactic tier** (`PyReprism.syntactic`, `pip install "PyReprism[ast]"`):
  tree-sitter ASTs for exact cyclomatic complexity and per-function metrics
  (`cyclomatic()`, `functions()`).
- **Semantic tier** (`PyReprism.semantic`, `pip install "PyReprism[semantic]"`):
  code embeddings for Type-4 clone detection (`embed()`, `similarity()`, and an
  `EmbeddingIndex` mirroring `FingerprintIndex`).
- **GitHub Action** (`action.yml`, "PyReprism Clone Gate") and a `Dockerfile`
  for the CLI, to gate pull requests on duplication.
- Parallel processing: `jobs=` on `batch.analyze`, `batch.transform`, and
  `clones.detect`, and a new `batch.map_files(paths, fn, jobs=...)` that runs any
  per-file function on all cores. `pyreprism scan` and `pyreprism clones` take
  `-j/--jobs` and use one process per CPU by default (`-j 1` for one process).
  Reports are identical for any number of jobs.
- Secondary file extensions map to their language: `.h` (C); `.cc`, `.cxx`,
  `.hpp`, `.hh`, `.hxx` (C++); `.mjs`, `.cjs`, `.mts`, `.cts`; `.pyi`; `.bash`,
  `.zsh`, `.ksh`; `.yml`; and others. These files were skipped before.

### Changed
- Faster tokenization (about 2.7x on one core) with identical tokens: each
  language's string, number, identifier, and operator patterns are joined into
  one pattern and compiled once, instead of being tried one by one at every
  position; line numbers are tracked incrementally. `stats` (and `scan`)
  count tokens as they are classified instead of building the token list
  (about 4x faster than before on one core; same results). `code_metrics` computes
  Halstead measures and complexity once instead of twice. Extension lookup no
  longer re-imports every language module (1.4 ms to under 1 µs per file).
- The Pygments engine is about 3x faster on large files with the same tokens:
  it merged tokens by repeated string concatenation and counted each token's
  line from the start of the file, both quadratic in file size.
- `Token` is now an immutable `NamedTuple` instead of a frozen dataclass, which
  makes tokens cheaper to create. Fields, attribute access, and immutability
  are unchanged; a `Token` now also compares equal to a plain tuple with the
  same values.

### Fixed
- `pyreprism --help` stated "160+ built-in languages"; it now says 187, matching
  `pyreprism languages`. A test keeps the two in sync.
- `pyreprism clones --max-duplication`: when stdout and stderr go to the same log
  (as in CI), the gate message could be written into the middle of the report's
  summary line. stdout is now flushed before the gate message.
- Defects found by validating token classes against tree-sitter parses:
  - `remove_comments` dropped text that a language's comment regex skips (e.g.
    the `/` in `#include "api/z3.h"`, a `{` in Scala). The base implementation
    now keeps it, and 20 modules that duplicated the old loop inherit it.
  - C, C++, Java, and CSS strings containing `/` were split, so `//` or `/*`
    inside them started a comment (Java text blocks are kept whole too).
  - Python: only a triple-quoted string that starts a line is a docstring
    (comment); `x = """..."""` and call arguments are strings.
  - JavaScript, TypeScript, JSX, TSX: template literals are strings, and
    regular-expression literals no longer start comments.
  - Pygments engine: C preprocessor directives were typed as comments, and
    Python docstrings as strings; both now follow the regex engine's policies.
- Strings containing comment delimiters (`"a//b"`, `"a#b"`, `'--'`) were split
  in 36 more languages, starting a comment inside the string: ActionScript,
  Ada, AppleScript, Asm6502, ASP.NET, AutoHotkey, AutoIt, Bro, CoffeeScript,
  Crystal, Elixir, Flow, GLSL, GraphQL, HPKP, HSTS, IchigoJam, Icon, Less,
  LiveScript, Lua (including `[[...]]` long strings), Nginx, NSIS, PL/SQL, Qore,
  Roboconf, Scheme (including `#\;` characters), SCSS (including unquoted
  `url(...)`), and SQL. Comments now follow each language's rules in Apache
  config, Dockerfiles, `.properties`, and Pug (own line only), Tcl (where a
  command starts), YAML (after whitespace), and ERB (`<%# %>` tags, not `#` in
  markup). A test checks every language with such a string.
- Defects found on the project-stratified evaluation sample: Go raw strings
  (`` `...` ``) containing `//` or `/*` became comments; in Bash, `#` inside a
  word (`$#`, `${#a}`, `a#b`) started a comment; a UTF-8 byte-order mark at the
  start of a file was counted as code, so the first line could not be a comment
  line (both engines); and a Python triple-quoted string on the line after an
  opening bracket, comma, or `=` was taken for a docstring.

## [0.2.0] - 2026-07-08

This release adds a static code-analysis toolkit on top of the tokenizer:
diff/PR analysis, complexity metrics, n-gram "naturalness", and clone/plagiarism
similarity — plus a comprehensive per-language test suite that hardened comment
handling across the board.

### Added
- **Fingerprinting & similarity** (`PyReprism.fingerprints`): winnowing k-gram
  fingerprints over the normalized token stream for clone/plagiarism detection —
  `fingerprint()`, `similarity()`/`containment()` (rename-invariant by default),
  and a `FingerprintIndex` for many-to-many detection over a corpus. CLI:
  `pyreprism similarity a b` and `pyreprism clones DIR --threshold`.
- **N-gram analysis & code naturalness** (`PyReprism.ngrams`): token/type n-gram
  extraction and frequency counts, plus an `NgramModel` (add-k smoothing,
  save/load) that measures cross-entropy / perplexity against a trained corpus
  ("naturalness of software"). CLI: `pyreprism ngrams` and
  `pyreprism perplexity --train`.
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

### Changed
- Adopted the standard `src/` layout with tests at the top level, consolidated
  all dependencies into `pyproject.toml` extras, and rewrote the landing page.
- Single-sourced the version from the package and automated releases: pushing a
  `vX.Y.Z` tag now publishes to PyPI (Trusted Publishing) and creates a GitHub
  Release. Added Python 3.13 to the CI matrix.
- Added a comprehensive, data-driven per-language comment test suite that
  requires every registered language to be covered.

### Fixed
- Fixed comment stripping in 8 more languages surfaced by the new test suite:
  `smalltalk` (kept the comment and deleted the code) and
  `eiffel`/`bro`/`coffeescript`/`io`/`nix`/`gherkin`/`gedcom` (trailing comments
  not removed and newlines dropped).
- Fixed a CLI argument-ordering incompatibility on Python ≤ 3.11 (options must
  follow positionals).

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

[Unreleased]: https://github.com/unlv-evol/PyReprism/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/unlv-evol/PyReprism/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/unlv-evol/PyReprism/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/unlv-evol/PyReprism/releases/tag/v0.1.0
[0.0.4]: https://github.com/unlv-evol/PyReprism/releases/tag/v0.0.4
