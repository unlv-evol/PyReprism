"""Comprehensive, data-driven comment-handling tests for every language.

Each language has one sample containing a comment written in that language's
own syntax. The tests assert that ``remove_comments`` strips the comment while
keeping the surrounding code, and that ``extract_comments`` returns it.

``test_every_registered_language_is_covered`` fails if a new language is added
without a sample here, so coverage cannot silently regress.
"""
import pytest

from PyReprism.languages import _load_all_languages
from PyReprism.languages.registry import LanguageRegistry

_load_all_languages()

# Markers embedded in every sample.
CODE_A, CODE_B, SECRET = "keepAA", "keepBB", "zzsecretzz"

# name -> source string containing ``SECRET`` inside a comment (language syntax).
SAMPLES = {
    'Abap': 'keepAA "zzsecretzz\nkeepBB\n',
    'ActionScript': 'keepAA //zzsecretzz\nkeepBB\n',
    'Ada': 'keepAA --zzsecretzz\nkeepBB\n',
    'ApacheConf': 'keepAA #zzsecretzz\nkeepBB\n',
    'Apl': 'keepAA ⍝zzsecretzz\nkeepBB\n',
    'AppleScript': 'keepAA #zzsecretzz\nkeepBB\n',
    'Arduino': 'keepAA //zzsecretzz\nkeepBB\n',
    'Arff': 'keepAA %zzsecretzz\nkeepBB\n',
    'Asciidoc': 'keepAA\n//zzsecretzz\nkeepBB\n',
    'Asm6502': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Aspnet': 'keepAA //zzsecretzz\nkeepBB\n',
    'AutoHotKey': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Autoit': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Bash': 'keepAA #zzsecretzz\nkeepBB\n',
    'Basic': "keepAA 'zzsecretzz\nkeepBB\n",
    'Batch': 'keepAA ::zzsecretzz\nkeepBB\n',
    'Bison': 'keepAA\n//zzsecretzz\nkeepBB\n',
    'Bro': 'keepAA #zzsecretzz\nkeepBB\n',
    'C': 'keepAA //zzsecretzz\nkeepBB\n',
    'CPP': 'keepAA //zzsecretzz\nkeepBB\n',
    'CSS': 'keepAA\n/*zzsecretzz*/\nkeepBB\n',
    'CSharp': 'keepAA //zzsecretzz\nkeepBB\n',
    'Clike': 'keepAA //zzsecretzz\nkeepBB\n',
    'Clojure': 'keepAA\n;zzsecretzz\nkeepBB\n',
    'CoffeeScript': 'keepAA #zzsecretzz\nkeepBB\n',
    'Crystal': 'keepAA #zzsecretzz\nkeepBB\n',
    'CssExtras': 'keepAA\n/*zzsecretzz*/\nkeepBB\n',
    'D': 'keepAA //zzsecretzz\nkeepBB\n',
    'Dart': 'keepAA //zzsecretzz\nkeepBB\n',
    'Diff': 'keepAA\n#zzsecretzz\nkeepBB\n',
    'Django': 'keepAA #zzsecretzz\nkeepBB\n',
    'Docker': 'keepAA #zzsecretzz\nkeepBB\n',
    'Eiffel': 'keepAA --zzsecretzz\nkeepBB\n',
    'Elixir': 'keepAA #zzsecretzz\nkeepBB\n',
    'ErLang': 'keepAA %zzsecretzz\nkeepBB\n',
    'Erb': 'keepAA #zzsecretzz\nkeepBB\n',
    'FSharp': 'keepAA //zzsecretzz\nkeepBB\n',
    'Flow': 'keepAA //zzsecretzz\nkeepBB\n',
    'ForTran': 'keepAA !zzsecretzz\nkeepBB\n',
    'Gedcom': 'keepAA\n#zzsecretzz\nkeepBB\n',
    'Gherkin': 'keepAA\n#zzsecretzz\nkeepBB\n',
    'Git': 'keepAA\n#zzsecretzz\nkeepBB\n',
    'Glsl': 'keepAA //zzsecretzz\nkeepBB\n',
    'Go': 'keepAA //zzsecretzz\nkeepBB\n',
    'GraphSql': 'keepAA #zzsecretzz\nkeepBB\n',
    'Groovy': 'keepAA //zzsecretzz\nkeepBB\n',
    'HTML': 'keepAA\n<!--zzsecretzz-->\nkeepBB\n',
    'Haml': 'keepAA\n-#zzsecretzz\nkeepBB\n',
    'Handlebars': 'keepAA\n{{!zzsecretzz}}\nkeepBB\n',
    'Haskell': 'keepAA --zzsecretzz\nkeepBB\n',
    'Haxe': 'keepAA //zzsecretzz\nkeepBB\n',
    'Hpkp': 'keepAA #zzsecretzz\nkeepBB\n',
    'Hsts': 'keepAA #zzsecretzz\nkeepBB\n',
    'INI': 'keepAA\n;zzsecretzz\nkeepBB\n',
    'IO': 'keepAA //zzsecretzz\nkeepBB\n',
    'IchigoJam': 'keepAA #zzsecretzz\nkeepBB\n',
    'Icon': 'keepAA #zzsecretzz\nkeepBB\n',
    'Inform7': 'keepAA //zzsecretzz\nkeepBB\n',
    'J': 'keepAA NB.zzsecretzz\nkeepBB\n',
    'Java': 'keepAA //zzsecretzz\nkeepBB\n',
    'JavaScript': 'keepAA //zzsecretzz\nkeepBB\n',
    'Jolie': 'keepAA //zzsecretzz\nkeepBB\n',
    'Json': 'keepAA //zzsecretzz\nkeepBB\n',
    'Jsx': 'keepAA //zzsecretzz\nkeepBB\n',
    'Julia': 'keepAA #zzsecretzz\nkeepBB\n',
    'Keyman': 'keepAA //zzsecretzz\nkeepBB\n',
    'Kotlin': 'keepAA //zzsecretzz\nkeepBB\n',
    'LOLCODE': 'keepAA BTW zzsecretzz\nkeepBB\n',
    'LUA': 'keepAA --zzsecretzz\nkeepBB\n',
    'Latex': 'keepAA %zzsecretzz\nkeepBB\n',
    'Less': 'keepAA //zzsecretzz\nkeepBB\n',
    'Liquid': 'keepAA\n{% comment %}zzsecretzz{% endcomment %}\nkeepBB\n',
    'LiveScript': 'keepAA #zzsecretzz\nkeepBB\n',
    'MEL': 'keepAA //zzsecretzz\nkeepBB\n',
    'MakeFile': 'keepAA #zzsecretzz\nkeepBB\n',
    'MarkDown': 'keepAA\n<!--zzsecretzz-->\nkeepBB\n',
    'MarkUp': 'keepAA\n<!--zzsecretzz-->\nkeepBB\n',
    'MarkupTemplating': 'keepAA\n<!--zzsecretzz-->\nkeepBB\n',
    'MatLab': 'keepAA %zzsecretzz\nkeepBB\n',
    'Mizar': 'keepAA ::zzsecretzz\nkeepBB\n',
    'Monkey': "keepAA 'zzsecretzz\nkeepBB\n",
    'N4js': 'keepAA //zzsecretzz\nkeepBB\n',
    'NASM': 'keepAA\n;zzsecretzz\nkeepBB\n',
    'NIM': 'keepAA #zzsecretzz\nkeepBB\n',
    'NIX': 'keepAA #zzsecretzz\nkeepBB\n',
    'NSIS': 'keepAA #zzsecretzz\nkeepBB\n',
    'Nginx': 'keepAA #zzsecretzz\nkeepBB\n',
    'ObjectiveC': 'keepAA //zzsecretzz\nkeepBB\n',
    'Ocaml': 'keepAA\n(*zzsecretzz*)\nkeepBB\n',
    'OpenCL': 'keepAA //zzsecretzz\nkeepBB\n',
    'Oz': 'keepAA %zzsecretzz\nkeepBB\n',
    'PHP': 'keepAA //zzsecretzz\nkeepBB\n',
    'PHPExtras': 'keepAA //zzsecretzz\nkeepBB\n',
    'PLSQL': 'keepAA --zzsecretzz\nkeepBB\n',
    'PariGP': 'keepAA \\\\zzsecretzz\nkeepBB\n',
    'Parser': 'keepAA #zzsecretzz\nkeepBB\n',
    'Pascal': 'keepAA //zzsecretzz\nkeepBB\n',
    'Perl': 'keepAA #zzsecretzz\nkeepBB\n',
    'PowerShell': 'keepAA #zzsecretzz\nkeepBB\n',
    'Processing': 'keepAA //zzsecretzz\nkeepBB\n',
    'Prolog': 'keepAA %zzsecretzz\nkeepBB\n',
    'Properties': 'keepAA #zzsecretzz\nkeepBB\n',
    'Protobuf': 'keepAA //zzsecretzz\nkeepBB\n',
    'Pug': 'keepAA //zzsecretzz\nkeepBB\n',
    'Puppet': 'keepAA #zzsecretzz\nkeepBB\n',
    'Pure': 'keepAA //zzsecretzz\nkeepBB\n',
    'Python': 'keepAA #zzsecretzz\nkeepBB\n',
    'Q': 'keepAA //zzsecretzz\nkeepBB\n',
    'Qore': 'keepAA //zzsecretzz\nkeepBB\n',
    'R': 'keepAA #zzsecretzz\nkeepBB\n',
    'Reason': 'keepAA //zzsecretzz\nkeepBB\n',
    'RenPy': 'keepAA #zzsecretzz\nkeepBB\n',
    'Rest': 'keepAA\n.. zzsecretzz\nkeepBB\n',
    'Rip': 'keepAA #zzsecretzz\nkeepBB\n',
    'Roboconf': 'keepAA #zzsecretzz\nkeepBB\n',
    'Ruby': 'keepAA #zzsecretzz\nkeepBB\n',
    'Rust': 'keepAA //zzsecretzz\nkeepBB\n',
    'SAS': 'keepAA\n/*zzsecretzz*/\nkeepBB\n',
    'SQL': 'keepAA //zzsecretzz\nkeepBB\n',
    'Sass': 'keepAA //zzsecretzz\nkeepBB\n',
    'Scala': 'keepAA //zzsecretzz\nkeepBB\n',
    'Scheme': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Scss': 'keepAA //zzsecretzz\nkeepBB\n',
    'SmallTalk': 'keepAA\n"zzsecretzz"\nkeepBB\n',
    'Smarty': 'keepAA\n{*zzsecretzz*}\nkeepBB\n',
    'Soy': 'keepAA //zzsecretzz\nkeepBB\n',
    'Stylus': 'keepAA\n//zzsecretzz\nkeepBB\n',
    'Swift': 'keepAA //zzsecretzz\nkeepBB\n',
    'Tcl': 'keepAA #zzsecretzz\nkeepBB\n',
    'Textile': 'keepAA #zzsecretzz\nkeepBB\n',
    'Tsx': 'keepAA //zzsecretzz\nkeepBB\n',
    'Twig': 'keepAA\n{#zzsecretzz#}\nkeepBB\n',
    'TypeScript': 'keepAA //zzsecretzz\nkeepBB\n',
    'Vbnet': "keepAA 'zzsecretzz\nkeepBB\n",
    'Velocity': 'keepAA ##zzsecretzz\nkeepBB\n',
    'Verilog': 'keepAA //zzsecretzz\nkeepBB\n',
    'Vhdl': 'keepAA --zzsecretzz\nkeepBB\n',
    'Vim': 'keepAA "zzsecretzz\nkeepBB\n',
    'VisualBasic': "keepAA 'zzsecretzz\nkeepBB\n",
    'Wasm': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Xeora': 'keepAA //zzsecretzz\nkeepBB\n',
    'Xojo': 'keepAA //zzsecretzz\nkeepBB\n',
    'Yaml': 'keepAA #zzsecretzz\nkeepBB\n',
    # --- generated (data-driven) languages: see languages/generated.py ---
    'Vala': 'keepAA //zzsecretzz\nkeepBB\n',
    'Solidity': 'keepAA //zzsecretzz\nkeepBB\n',
    'Wgsl': 'keepAA //zzsecretzz\nkeepBB\n',
    'Move': 'keepAA //zzsecretzz\nkeepBB\n',
    'Sway': 'keepAA //zzsecretzz\nkeepBB\n',
    'Pony': 'keepAA //zzsecretzz\nkeepBB\n',
    'Thrift': 'keepAA //zzsecretzz\nkeepBB\n',
    'Zig': 'keepAA //zzsecretzz\nkeepBB\n',
    'Gleam': 'keepAA //zzsecretzz\nkeepBB\n',
    'Toml': 'keepAA #zzsecretzz\nkeepBB\n',
    'Capnp': 'keepAA #zzsecretzz\nkeepBB\n',
    'CMake': 'keepAA #zzsecretzz\nkeepBB\n',
    'Fish': 'keepAA #zzsecretzz\nkeepBB\n',
    'Awk': 'keepAA #zzsecretzz\nkeepBB\n',
    'Janet': 'keepAA #zzsecretzz\nkeepBB\n',
    'Hcl': 'keepAA #zzsecretzz\nkeepBB\n',
    'Elm': 'keepAA --zzsecretzz\nkeepBB\n',
    'PureScript': 'keepAA --zzsecretzz\nkeepBB\n',
    'Racket': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Fennel': 'keepAA ;zzsecretzz\nkeepBB\n',
    'Red': 'keepAA ;zzsecretzz\nkeepBB\n',
    # --- second batch: more families + dedicated scanners ---
    'Cadence': 'keepAA //zzsecretzz\nkeepBB\n',
    'Chapel': 'keepAA //zzsecretzz\nkeepBB\n',
    'Tact': 'keepAA //zzsecretzz\nkeepBB\n',
    'Carbon': 'keepAA //zzsecretzz\nkeepBB\n',
    'Hare': 'keepAA //zzsecretzz\nkeepBB\n',
    'Cue': 'keepAA //zzsecretzz\nkeepBB\n',
    'Ballerina': 'keepAA //zzsecretzz\nkeepBB\n',
    'Jsonnet': 'keepAA //zzsecretzz\nkeepBB\n',
    'Odin': 'keepAA //zzsecretzz\nkeepBB\n',
    'V': 'keepAA //zzsecretzz\nkeepBB\n',
    'Jai': 'keepAA //zzsecretzz\nkeepBB\n',
    'Vyper': 'keepAA #zzsecretzz\nkeepBB\n',
    'Starlark': 'keepAA #zzsecretzz\nkeepBB\n',
    'Nushell': 'keepAA #zzsecretzz\nkeepBB\n',
    'Nickel': 'keepAA #zzsecretzz\nkeepBB\n',
    'Just': 'keepAA #zzsecretzz\nkeepBB\n',
    'Dhall': 'keepAA --zzsecretzz\nkeepBB\n',
    'Idris': 'keepAA --zzsecretzz\nkeepBB\n',
    'Futhark': 'keepAA --zzsecretzz\nkeepBB\n',
    'Lean': 'keepAA --zzsecretzz\nkeepBB\n',
}

# Languages whose comment model doesn't fit the shared sample; tested separately.
# COBOL is column-sensitive (see test_generated_languages.py).
SPECIAL = {'CSP', 'BrainFuck', 'Cobol'}


@pytest.mark.parametrize('name', sorted(SAMPLES))
def test_remove_comments_strips_comment_and_keeps_code(name):
    cls = LanguageRegistry.get(name)
    assert cls is not None, f"{name} is not registered"
    out = cls.remove_comments(SAMPLES[name])
    assert CODE_A in out and CODE_B in out, f"{name}: code was removed -> {out!r}"
    assert SECRET not in out, f"{name}: comment was not stripped -> {out!r}"


@pytest.mark.parametrize('name', sorted(SAMPLES))
def test_extract_comments_returns_the_comment(name):
    cls = LanguageRegistry.get(name)
    comments = cls.extract_comments(SAMPLES[name])
    assert any(SECRET in c for c in comments), f"{name}: comment not extracted -> {comments!r}"


@pytest.mark.parametrize('name', sorted(SAMPLES))
def test_remove_comments_is_idempotent(name):
    cls = LanguageRegistry.get(name)
    once = cls.remove_comments(SAMPLES[name])
    assert cls.remove_comments(once) == once, f"{name}: remove_comments not idempotent"


def test_csp_has_no_comment_syntax():
    # CSP is header text with no comments; nothing is treated as a comment
    # (not even the "//" in a URL).
    csp = LanguageRegistry.get('CSP')
    out = csp.remove_comments("default-src 'self'; script-src https://example.com")
    assert "https://example.com" in out
    assert "default-src 'self'" in out


def test_brainfuck_keeps_commands_strips_prose():
    # In Brainfuck every non-command character is a comment.
    bf = LanguageRegistry.get('BrainFuck')
    out = bf.remove_comments('+++ hello , world [.]')
    assert '+++' in out and ',' in out and '[' in out and '.' in out
    assert 'hello' not in out and 'world' not in out


# Block comments that span several lines (the SAMPLES above are mostly one line).
MULTILINE_BLOCKS = {
    'C': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'CPP': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'Java': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'JavaScript': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'Go': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'Rust': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'CSS': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'PHP': 'keepAA\n/*\nzzsecretzz\n*/\nkeepBB\n',
    'Ocaml': 'keepAA\n(*\nzzsecretzz\n*)\nkeepBB\n',
    'Pascal': 'keepAA\n(*\nzzsecretzz\n*)\nkeepBB\n',
    'HTML': 'keepAA\n<!--\nzzsecretzz\n-->\nkeepBB\n',
    'MarkDown': 'keepAA\n<!--\nzzsecretzz\n-->\nkeepBB\n',
}


@pytest.mark.parametrize('name', sorted(MULTILINE_BLOCKS))
def test_multiline_block_comments(name):
    cls = LanguageRegistry.get(name)
    out = cls.remove_comments(MULTILINE_BLOCKS[name])
    assert CODE_A in out and CODE_B in out, f"{name}: code removed -> {out!r}"
    assert SECRET not in out, f"{name}: block comment not stripped -> {out!r}"


@pytest.mark.parametrize('quote', ['"""', "'''"])
@pytest.mark.parametrize('name', ['Python', 'Django'])
def test_triple_quoted_block_comments(name, quote):
    # Python (and Django, which processes .py files) treats triple-quoted
    # string blocks as removable docstring "comments".
    cls = LanguageRegistry.get(name)
    out = cls.remove_comments(f"x = 1\n{quote}\n{SECRET}\n{quote}\ny = 2\n")
    assert 'x = 1' in out and 'y = 2' in out
    assert SECRET not in out


def test_every_registered_language_is_covered():
    registered = set(LanguageRegistry.all())
    covered = set(SAMPLES) | SPECIAL
    missing = registered - covered
    assert not missing, (
        f"these registered languages have no comment test: {sorted(missing)}. "
        f"Add a sample to SAMPLES in this file."
    )
    stale = covered - registered - SPECIAL
    assert not stale, f"these samples reference unregistered languages: {sorted(stale)}"
