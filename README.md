[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/pyreprism)](https://pepy.tech/project/pyreprism)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=license)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=license)
[![FOSSA Status](https://app.fossa.com/api/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism.svg?type=shield&issueType=security)](https://app.fossa.com/projects/custom%2B46484%2Fgithub.com%2Funlv-evol%2FPyReprism?ref=badge_shield&issueType=security)
[![Documentation Status](https://readthedocs.org/projects/pyreprism/badge/?version=latest)](https://pyreprism.readthedocs.io/en/latest/?badge=latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PyReprism)
![CI](https://github.com/unlv-evol/PyReprism/actions/workflows/ci.yml/badge.svg)
![Publish](https://github.com/unlv-evol/PyReprism/actions/workflows/publish.yml/badge.svg)
[![codecov](https://codecov.io/gh/unlv-evol/PyReprism/graph/badge.svg?token=J2JV31837H)](https://codecov.io/gh/unlv-evol/PyReprism)
![PyPI - Version](https://img.shields.io/pypi/v/pyreprism)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unlv-evol/pyreprism/main)
[![SWH](https://archive.softwareheritage.org/badge/origin/https://pypi.org/project/PyReprism//)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://pypi.org/project/PyReprism/)

> [!IMPORTANT]
> **SANER 2027 Tool Demo Track reviewers:** the demonstration video is at
> **[https://youtu.be/IXc-NP5t4GU](https://youtu.be/IXc-NP5t4GU)**.
> The version evaluated in the paper is tagged
> [`saner2027-artifact`](https://github.com/unlv-evol/PyReprism/tree/saner2027-artifact);
> the latest release is on [PyPI](https://pypi.org/project/PyReprism/).

# PyReprism

PyReprism is a Python framework that helps researchers and developers the task of source code preprocessing. With PyReprism, you can easily match, extract, count, and remove comments, whitespaces, operators, numbers and other language specific constructs from over **187 programming languages and file extensions** — and **500+** with the optional Pygments backend.

Everything is derived from one **lossless token stream**, and the same substrate
anchors a **fidelity ladder** of three optional-cost tiers: a zero-dependency
**lexical** tier (default), an optional **syntactic** tier (tree-sitter ASTs for
precise per-function metrics), and an optional **semantic** tier (code embeddings
for Type-4 clone detection). The core stays dependency-free; you climb the ladder
only when a task needs it.

## Install
```shell
pip install PyReprism                 # zero-dependency lexical core

# optional tiers (install only what you need):
pip install "PyReprism[accurate]"     # Pygments backend (higher lexical fidelity)
pip install "PyReprism[ast]"          # syntactic tier (tree-sitter)
pip install "PyReprism[semantic]"     # semantic tier (code embeddings)
```

### Run with Docker

No Python install required. The image ships the 187-language lexical core plus
the Pygments backend (the heavier `[ast]`/`[semantic]` tiers are omitted to keep
it small). Mount your code at `/work`:

```shell
docker build -t pyreprism .

# fail CI above 5% duplication, emit SARIF for code scanning
docker run --rm -v "$PWD:/work" pyreprism clones . --reporter sarif --max-duplication 5

# per-language metrics as JSON
docker run --rm -v "$PWD:/work" pyreprism scan . --json
```

### GitHub Action

Gate pull requests on code duplication in a few lines. The action runs
`pyreprism clones`, writes a report, and fails the job when duplication exceeds
your threshold:

```yaml
- uses: actions/checkout@v4
- uses: unlv-evol/PyReprism@v1.0.0    # pin to a release tag or commit SHA
  with:
    paths: .
    reporter: sarif
    output: pyreprism-clones.sarif
    max_duplication: 5                # fail the job above 5% duplicated lines
    near: true                        # also flag Type-3 near-duplicate files

# optional: surface the clones in the repo's Security > Code scanning tab
- uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: pyreprism-clones.sarif
```

Inputs: `paths`, `reporter` (`console`/`json`/`sarif`/`markdown`/`html`),
`output`, `max_duplication`, `min_tokens`, `min_lines`, `near`, `semantic`,
`lang`, and `extra_args`.

## Quick Usage

The simplest entry point is the top-level API. Pass `lang` as a language name
(`"python"`), a file extension (`".py"`), or a language class.

```python
import PyReprism as pr

source = """
# single line comment
x = 5 + 6
print(x)  # inline comment
"""

pr.remove_comments(source, lang="python")   # -> code with comments stripped
pr.extract_comments(source, lang="python")  # -> ['# single line comment', '# inline comment']
pr.count_comments(source, lang="python")    # -> 2
```

Every construct supports the same **match / extract / count / remove** verbs:

```python
code = 'total = price * 42 + tax  # compute'

pr.extract_numbers(code, lang="python")      # -> ['42']
pr.extract_keywords(code, lang="python")     # -> []
pr.extract_identifiers(code, lang="python")  # -> ['total', 'price', 'tax', 'compute']
pr.remove_numbers(code, lang="python")       # -> 'total = price *  + tax  # compute'
pr.extract_strings('s = "hi"', lang="python")  # -> ['"hi"']
```

`match_*` returns positioned `Token`s (`type`, `value`, `start`, `end`, `line`):

```python
for tok in pr.match_comments(source, lang="python"):
    print(tok.line, tok.value)
```

### Tokenize

`tokenize()` returns a lossless, typed token stream (comment/string/number/
keyword/identifier/operator/whitespace/other):

```python
for tok in pr.tokenize("x = 5 + y  // c", lang="clike"):
    print(tok.type, repr(tok.value))
```

### Pipelines

Chain removal steps in one call:

```python
pr.preprocess(source, lang="java",
              steps=["comments", "strings", "whitespace"])
```

Valid steps: `comments`, `strings`, `numbers`, `operators`, `keywords`, `whitespace`.

### Code metrics

```python
s = pr.stats(source, lang="python")
s.code_lines, s.comment_lines, s.blank_lines
s.comment_to_code_ratio, s.comment_density
s.as_dict()   # includes per-token-type counts, ready for JSON / dataframes
```

Complexity metrics (computed from the token stream):

```python
pr.halstead(source, lang="python").volume        # Halstead volume/difficulty/effort/bugs
pr.cyclomatic_complexity(source, lang="python")  # approximate McCabe complexity
pr.maintainability_index(source, lang="python")  # 0–100 (higher is better)
pr.code_metrics(source, lang="python")           # everything above in one dict
```

On the CLI: `pyreprism stats --full file.py` (add `--json` for machine output).

### Similarity & clone / plagiarism detection

Winnowing k-gram fingerprints over the *normalized* token stream, so matches
survive variable renaming and literal changes (Type-2 clones):

```python
from PyReprism import fingerprints as fp

fp.similarity(code_a, code_b, "python")     # 0.0–1.0 (Jaccard of fingerprints)
fp.containment(code_a, code_b, "python")    # how much of A appears in B

index = fp.FingerprintIndex()               # many-to-many clone detection
index.add_paths("submissions/")
index.similar_pairs(threshold=0.7)          # -> [(file_a, file_b, score), ...]
```

On the CLI: `pyreprism similarity a.py b.py` and
`pyreprism clones submissions/ --threshold 0.7`.

#### Located clones & reports (a jscpd-style duplication detector)

Beyond a similarity score, `PyReprism.clones` reports **which line ranges are
duplicated** between files (Rabin-Karp over the normalized token stream), and
renders a **unified report** across all three rungs of the fidelity ladder:

```python
from PyReprism import clones, reporters

report = clones.detect("src/",
                       min_tokens=50, min_lines=5,   # clone-size floor (jscpd-style)
                       near=True,                    # + Type-3 near-duplicate files
                       semantic=True)                # + Type-4 semantic clones
report.duplication_pct                               # % duplicated lines
for c in report.clones:
    print(c.kind, c.a.path, c.a.start_line, c.b.path, c.b.start_line)
    # kind is 'exact' (T1/2, located), 'near' (T3), or 'semantic' (T4)

print(reporters.to_sarif(report))       # GitHub code scanning
print(reporters.to_markdown(report))    # PR comment
print(reporters.to_json(report))
print(reporters.to_html(report))        # self-contained HTML report page
```

Every clone — **including semantic (Type-4)** ones — flows through the same
reporters, each kind tagged with its own SARIF rule id
(`pyreprism/exact-clone`, `.../near-clone`, `.../semantic-clone`), so CI can treat
lexical and semantic duplication separately. The **HTML reporter** renders a
self-contained, theme-aware page — a duplication meter with a CI-gate marker,
per-kind counts, and a filterable card per clone with located line ranges,
score, rule id, and a highlighted side-by-side snippet. On the CLI:

```shell
pyreprism clones src/                                  # located exact clones (console)
pyreprism clones src/ --near --semantic                # add Type-3 and Type-4
pyreprism clones src/ --reporter sarif  > clones.sarif # for GitHub code scanning
pyreprism clones src/ --reporter html --max-duplication 5 > clones.html   # HTML report + CI gate
pyreprism clones src/ --max-duplication 5              # exit non-zero above 5% (CI gate)
pyreprism clones src/ -j 1                             # one process (default: one per CPU)
```

Fingerprints and located clones detect Type-1/2/3. For **Type-4** clones (same
behavior, different code), `--semantic` embeds functions with the optional
[semantic tier](#higher-fidelity-tiers-syntactic-ast--semantic-embeddings) and
adds them to the same report.

### N-grams & code "naturalness"

Token n-grams (over token text or, structurally, over token *types*) and an
n-gram language model that measures how predictable/"natural" code is
(Hindle et al.):

```python
from PyReprism import ngrams

ngrams.ngram_counts(source, "python", n=3).most_common(10)
ngrams.ngrams(source, "python", n=2, types=True)      # structural n-grams

model = ngrams.train("corpus/", n=3)                  # train on a code corpus
model.perplexity(ngrams.token_sequence(source, "python"))   # lower = more natural
model.save("model.json")
```

On the CLI: `pyreprism ngrams file.py -n 3 --top 20` and
`pyreprism perplexity --train corpus/ file.py`.

### Normalization for ML / clone detection

Canonicalize code so that only its structure remains — rename identifiers to
`VAR1, VAR2, …`, mask string/number literals, and drop comments:

```python
pr.normalize("total = price * 42  # cost", lang="python")
# -> 'VAR1 = VAR2 * 0'
```

Every part is toggleable (`rename_identifiers`, `mask_numbers`, `mask_strings`,
`drop_comments`, `collapse_whitespace`). To strip comments while keeping line
numbers stable (useful for tools that map back to source):

```python
pr.blank_comments(source, lang="python")   # comment content removed, newlines kept
```

### Accuracy: choose a backend

By default PyReprism uses its own zero-dependency regex engine (fast, no installs).
For higher accuracy — e.g. correctly ignoring a `#` inside a string — pass
`engine="pygments"` (install the optional extra with `pip install pyreprism[accurate]`):

```python
src = 'url = "http://x#frag"  # real comment'

pr.remove_comments(src, lang="python")                     # regex (default)
pr.remove_comments(src, lang="python", engine="pygments")  # keeps the URL, drops the comment
```

`engine` accepts `"regex"` (default), `"pygments"`, or `"auto"` (use pygments if
installed, else regex). It works on every operation — `remove_*`, `extract_*`,
`count_*`, `tokenize`, `normalize`, `stats`, `preprocess` — and on the CLI via
`--engine`.

When Pygments is installed, a language or extension that has no built-in module
also resolves through an on-demand Pygments fallback, extending coverage to
**500+** languages (`pr.get_language(".zig")`, `pr.remove_comments(src, lang="solidity")`).
List what is reachable with `pyreprism languages` (built-in) and
`pyreprism languages --pygments` (the fallback tier).

### Higher-fidelity tiers: syntactic (AST) & semantic (embeddings)

The lexical core is fast and broad but approximate. For tasks that need more, the
same substrate feeds two optional tiers — install only what you need.

**Syntactic tier** (`pip install "PyReprism[ast]"`) parses a real tree-sitter AST
for exact, **per-function** metrics that a token stream cannot provide:

```python
from PyReprism import syntactic as ast

ast.cyclomatic(src, "java")     # precise McCabe complexity (decision nodes)
ast.functions(src, "python")    # -> [FunctionInfo(name, start_line, cyclomatic), ...]
```

**Semantic tier** (`pip install "PyReprism[semantic]"`) embeds code with a
code-search transformer to catch **Type-4** clones (same behavior, different code)
that token fingerprints cannot — it mirrors the `FingerprintIndex` API:

```python
from PyReprism import semantic

semantic.similarity(code_a, code_b)         # cosine similarity in embedding space

idx = semantic.EmbeddingIndex()
idx.add_paths("submissions/")
idx.similar_pairs(threshold=0.8)            # semantic near-duplicate pairs
idx.query(code, k=5)                        # k most similar indexed snippets
```

Both tiers degrade gracefully: if the extra isn't installed, `available()` returns
`False` and the lexical core is unaffected. Use the lexical tier for screening,
the syntactic tier for precise/per-function metrics, and the semantic tier for
Type-4 clones.

### Batch / whole-directory processing

Analyze or transform an entire source tree (junk folders like `.git`,
`node_modules`, `venv` are skipped automatically):

```python
from PyReprism import batch

report = batch.analyze("myproject/")     # walk the tree, compute metrics
report.totals()                          # aggregate line/token counts
report.by_language()                     # per-language breakdown
report.to_json(); report.to_csv()        # export for dataframes / notebooks

# Bulk-transform into a mirrored output directory:
batch.transform("myproject/", lambda text, lang: lang.remove_comments(text),
                output="stripped/")
```

Files are independent, so these calls can use every core: pass `jobs=0` (one
process per CPU) or `jobs=N` to `batch.analyze`, `batch.transform`,
`batch.map_files`, and `clones.detect`; results are identical to a serial run.
With `jobs` other than 1, functions you pass must be picklable (defined at
module level, not lambdas):

```python
def metrics_and_copy(text, lang):              # any per-file analysis
    return lang.code_metrics(text), lang.normalize(text)

for path, lang, (metrics, normalized) in batch.map_files("myproject/", metrics_and_copy, jobs=0):
    ...
```

### Process diffs / pull requests

Parse a unified (`git`) diff and analyze the *changed code* per file, language-aware:

```python
from PyReprism import diffs

d = diffs.parse(diff_text)          # git diff / .diff / .patch text

report = diffs.diff_stats(d)        # churn split into code vs comment vs blank
report.totals(); report.to_csv()

diffs.cosmetic_files(d)             # files whose change is comment/whitespace-only

f = d.files[0]
f.language                          # detected from the file path
f.added_text(); f.removed_text()    # reconstructed changed code
f.normalize("added")               # canonicalize the added code for ML
f.extract_comments("added")
```

For accuracy where a comment/string spans a hunk boundary, set
`f.new_source` / `f.old_source` to the full file contents (e.g. from `git show`)
and the changed lines are classified against the whole file. On the CLI:

```shell
git diff | pyreprism diff --per-file      # churn report
git diff | pyreprism diff --json
git diff | pyreprism diff --cosmetic      # list comment/whitespace-only changes
```

### Detect the language from a filename

```python
cls = pr.detect_language(filename="src/main.go")   # -> Go language class
```

### Language-independent whitespace normalization

```python
pr.remove_whitespaces("x = 5 + 6\n\n\nprint(x)")  # -> 'x=5+6\nprint(x)'
```

You can also import a language class directly if you prefer:

```python
from PyReprism.languages import Python
Python.remove_comments(source)
```

## Command line

Installing PyReprism also provides a `pyreprism` command (works on stdin/stdout,
files, and globs; the language is auto-detected from a file's extension):

```shell
pyreprism remove comments file.py
cat file.go | pyreprism remove comments --lang go
pyreprism extract comments "src/**/*.py" --json
pyreprism count comments file.py --lang python
pyreprism preprocess --steps comments,strings,whitespace file.java
pyreprism tokenize --json file.py
pyreprism stats --json file.py                 # line/token metrics
pyreprism normalize file.py                    # canonicalize for ML
pyreprism remove comments file.py --in-place   # rewrite in place
pyreprism scan myproject/ --csv                # aggregate metrics over a tree
pyreprism remove comments src/ --output out/   # bulk-transform a directory
pyreprism languages                            # list built-in languages
pyreprism languages --pygments                 # list the Pygments fallback tier
```

Equivalently: `python -m PyReprism ...`.

It can also be wired into [pre-commit](https://pre-commit.com) via the bundled
`.pre-commit-hooks.yaml` (`pyreprism-strip-comments`, `pyreprism-normalize-whitespace`).
These hooks rewrite files, so scope them with `files:`/`exclude:`.

Read the [docs](https://pyreprism.readthedocs.io) for more usage examples.

## Stability and versioning

PyReprism 1.0 is the first stable release. From 1.0 on, releases follow
[semantic versioning](https://semver.org): the public API (the top-level
functions, the language classes, `Token`/`TokenType`, `CodeStats`, the
`batch`, `diffs`, `fingerprints`, `ngrams`, `clones`, `reporters`, `syntactic`,
and `semantic` modules) and the `pyreprism` command line change incompatibly
only in a new major version. Modules whose names start with an underscore are
internal. Token classifications may still change in minor releases when they
fix a lexer defect; the [changelog](CHANGELOG.md) lists every such change.

## Performance

Tokenization is a single compiled pattern per language, and directory-level
work can use every core: `pyreprism scan` and `pyreprism clones` do so by
default (`-j N` to change it), and the Python API takes `jobs=` (`jobs=0` for
one process per CPU).
On an 8-core Apple M3, `pyreprism scan` processes about 2,000 files per second;
a lexical workflow that replaces cloc, lizard, and jscpd (line counts,
complexity, and clones over the same files) runs 3.0x faster on one core
and 5.7x faster on 8 cores than the three tools together.

## How to Contribute
We invite you to help us build this tool and make it more extensive. Contribution is open to OSS community.

```shell
$ git clone https://github.com/unlv-evol/PyReprism.git
$ cd PyReprism
```
**(Optional)** It is suggested to make use of virtualenv. Therefore, before installing the requirements run:

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

Then, install the package in editable mode with its development tooling:

```shell
$ pip install -e ".[dev]"
```
For more information on how to contribute, read our [contributing guidelines](CONTRIBUTING.md).

## Issues
If you experience any issue, feel free to report it.
