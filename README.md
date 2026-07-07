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

# PyReprism

PyReprism is a Python framework that helps researchers and developers the task of source code preprocessing. With PyReprism, you can easily match, extract, count, and remove comments, whitespaces, operators, numbers and other language specific constructs from over **150 programming languages and file extensions**.

## Install
```shell
pip install PyReprism
```
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
pyreprism count comments --lang python file.py
pyreprism preprocess --steps comments,strings,whitespace file.java
pyreprism tokenize --json file.py
pyreprism stats --json file.py                 # line/token metrics
pyreprism normalize file.py                    # canonicalize for ML
pyreprism remove comments --in-place file.py   # rewrite in place
pyreprism scan myproject/ --csv                # aggregate metrics over a tree
pyreprism remove comments src/ --output out/   # bulk-transform a directory
pyreprism languages                            # list supported languages
```

Equivalently: `python -m PyReprism ...`.

It can also be wired into [pre-commit](https://pre-commit.com) via the bundled
`.pre-commit-hooks.yaml` (`pyreprism-strip-comments`, `pyreprism-normalize-whitespace`).
These hooks rewrite files, so scope them with `files:`/`exclude:`.

Read the [docs](https://pyreprism.readthedocs.io) for more usage examples. 

NB: The beta versions of PyReprism is still unstable, but we are working 24/7 to ensure the tool is usable.

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
