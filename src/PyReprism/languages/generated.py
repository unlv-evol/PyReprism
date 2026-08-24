"""Data-driven, zero-dependency language modules generated from a family table.

Many languages share a comment syntax ("family"): C-style ``// /* */``, hash
``#``, Haskell-style ``-- {- -}``, Lisp-style ``;``, and so on. Rather than write a
near-identical module per language, we declare each new language as a row
``(ClassName, extension, family, keywords)`` and synthesize a real
:class:`~PyReprism.languages.base.BaseLanguage` subclass for it. These are
first-class, registered, zero-dependency languages (unlike the Pygments fallback
in :mod:`~PyReprism.languages.dynamic`); each has a comment-handling test in the
suite, so they are *validated*, not merely supported.

To add a language: append a row to :data:`LANGUAGES` (and a sample to the test
suite's ``SAMPLES``). To add a comment family: add an entry to :data:`FAMILIES`.
"""
import re

from ._scanners import NestedCStyleLanguage
from .base import BaseLanguage
from .registry import LanguageRegistry

# Each family maps to (comment-alternatives, characters that end a plain-code run,
# string-literal style). The generated comment regex keeps strings intact and only
# treats real comment delimiters as comments -- the same idiom the hand-written
# modules use (see e.g. languages/go.py).
#   strings='both'   -> both '...' and "..." are string literals
#   strings='double' -> only "..." is a string (for Lisp-family, where ' is quote)
FAMILIES = {
    # C-style: line // and block /* */
    'cstyle':    (r'//.*?$|/\*[\s\S]*?\*/', '/', 'both'),
    # // line comments only (e.g. Zig, Gleam -- no block comments)
    'slashline': (r'//.*?$', '/', 'both'),
    # # line comments (Toml, CMake, Fish, ...)
    'hash':      (r'#.*?$', '#', 'both'),
    # HCL/Terraform: # or // line comments, plus /* */ blocks
    'hcl':       (r'#.*?$|//.*?$|/\*[\s\S]*?\*/', '#/', 'both'),
    # Haskell-style: -- line and {- -} block (Elm, PureScript)
    'dashbrace': (r'--.*?$|\{-[\s\S]*?-\}', '-{', 'both'),
    # Racket/Scheme-style: ; line and #| |# block
    'racket':    (r';.*?$|#\|[\s\S]*?\|#', ';#', 'double'),
    # ; line comments only (Fennel, Red, ...)
    'semicolon': (r';.*?$', ';', 'double'),
    # -- line comments only (Futhark, ...); no block form
    'dashline':  (r'--.*?$', '-', 'double'),
    # Lean 4: -- line and /- -/ block (treated non-nested; see NESTED for nesting)
    'lean':      (r'--.*?$|/-[\s\S]*?-/', '-/', 'double'),
}


def _build_comment_regex(family: str) -> re.Pattern:
    comment_alt, stop_chars, strings = FAMILIES[family]
    if strings == 'double':
        str_alt = r'"(?:\\.|[^"\\])*"'
    else:
        str_alt = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    # A code run: a string literal, or one char followed by non-delimiter chars.
    # The negated class stops at the family's comment starters and at quotes/backslash
    # so the next comment/string is re-examined at its own start.
    noncomment = rf'{str_alt}|.[^{stop_chars}\\\'"]*'
    pattern = rf'(?P<comment>{comment_alt})|(?P<noncomment>{noncomment})'
    return re.compile(pattern, re.DOTALL | re.MULTILINE)


# (ClassName, file extension, comment family, keywords)
LANGUAGES = [
    # --- C-style ( // + /* */ ) ---
    ('Vala',       '.vala',   'cstyle',    'if|else|while|for|foreach|do|switch|case|break|continue|return|class|interface|struct|enum|namespace|public|private|protected|internal|static|const|void|var|new|delete|null|true|false|this|base|using|out|ref|owned|unowned|async|yield'),
    ('Solidity',   '.sol',    'cstyle',    'pragma|contract|library|interface|function|modifier|event|struct|enum|mapping|address|uint|uint256|int|bool|string|bytes|memory|storage|calldata|public|private|internal|external|view|pure|payable|returns|return|if|else|for|while|do|require|revert|emit|new|import|is|constructor|using'),
    ('Wgsl',       '.wgsl',   'cstyle',    'fn|let|var|const|struct|return|if|else|for|while|loop|break|continue|switch|case|default|bool|i32|u32|f32|f16|vec2|vec3|vec4|mat4x4|array|ptr|type|override|true|false|discard'),
    ('Move',       '.move',   'cstyle',    'module|script|fun|public|native|struct|has|copy|drop|store|key|let|mut|if|else|while|loop|return|abort|use|const|move|copy|acquires|as|spec'),
    ('Sway',       '.sw',     'cstyle',    'contract|library|script|predicate|fn|pub|struct|enum|impl|trait|use|let|mut|if|else|match|while|for|return|const|storage|abi|self|Self|true|false'),
    ('Pony',       '.pony',   'cstyle',    'actor|class|primitive|interface|trait|struct|type|fun|be|new|var|let|if|then|else|elseif|end|while|do|for|in|match|return|error|recover|consume|iso|trn|ref|val|box|tag|true|false'),
    ('Thrift',     '.thrift', 'cstyle',    'namespace|include|struct|union|exception|service|enum|typedef|const|required|optional|oneway|void|bool|byte|i16|i32|i64|double|string|binary|list|set|map|throws|extends'),
    # --- // line only ---
    ('Zig',        '.zig',    'slashline', 'const|var|fn|pub|return|if|else|while|for|switch|break|continue|defer|errdefer|try|catch|struct|enum|union|error|comptime|inline|test|and|or|orelse|unreachable|null|undefined|true|false|void|type|anytype|usingnamespace|export|extern'),
    ('Gleam',      '.gleam',  'slashline', 'fn|pub|let|const|type|case|if|else|import|as|use|assert|todo|panic|try|opaque|external|True|False|Nil|Ok|Error'),
    # --- # line ---
    ('Toml',       '.toml',   'hash',      'true|false'),
    ('Capnp',      '.capnp',  'hash',      'struct|enum|interface|union|group|const|annotation|import|using|extends|Void|Bool|Int8|Int16|Int32|Int64|UInt8|UInt16|UInt32|UInt64|Float32|Float64|Text|Data|List'),
    ('CMake',      '.cmake',  'hash',      'if|elseif|else|endif|foreach|endforeach|while|endwhile|function|endfunction|macro|endmacro|set|unset|option|include|add_executable|add_library|target_link_libraries|find_package|message|return|break|continue'),
    ('Fish',       '.fish',   'hash',      'if|else|end|switch|case|for|in|while|function|return|begin|and|or|not|set|test|command|builtin|break|continue'),
    ('Awk',        '.awk',    'hash',      'BEGIN|END|if|else|while|for|do|break|continue|next|exit|return|function|print|printf|getline|delete|in|length|substr|split|gsub|sub|match'),
    ('Janet',      '.janet',  'hash',      'def|var|defn|defmacro|fn|do|if|when|unless|cond|case|while|for|each|let|set|quote|quasiquote|import|require|true|false|nil'),
    # --- HCL / Terraform ( # or // line + /* */ ) ---
    ('Hcl',        '.tf',     'hcl',       'resource|provider|variable|output|module|data|locals|terraform|true|false|null|for|in|if'),
    # --- Haskell-style ( -- line + {- -} block ) ---
    ('Elm',        '.elm',    'dashbrace', 'module|import|exposing|type|alias|port|if|then|else|case|of|let|in|as|True|False|Nothing|Just'),
    ('PureScript', '.purs',   'dashbrace', 'module|import|as|hiding|class|instance|where|data|newtype|type|forall|if|then|else|case|of|let|in|do|derive|true|false'),
    # --- Lisp-family ( ; line + #| |# block ) ---
    ('Racket',     '.rkt',    'racket',    'define|lambda|let|let*|letrec|if|cond|case|when|unless|begin|set!|quote|quasiquote|require|provide|struct|module|for|and|or|not|else|true|false'),
    # --- ; line only ---
    ('Fennel',     '.fnl',    'semicolon', 'fn|lambda|local|var|set|let|if|when|do|for|each|while|match|global|require|import-macros|and|or|not|true|false|nil'),
    ('Red',        '.red',    'semicolon', 'if|either|unless|while|until|loop|repeat|foreach|func|function|does|has|make|return|break|continue|true|false|none'),
    # --- more C-style ( // + /* */ ) ---
    ('Cadence',    '.cdc',    'cstyle',    'pub|priv|let|var|fun|struct|resource|interface|contract|event|enum|case|if|else|while|for|in|return|break|continue|import|from|pre|post|access|self|init|destroy|create|emit|true|false|nil'),
    ('Chapel',     '.chpl',   'cstyle',    'proc|iter|class|record|module|var|const|param|type|if|else|for|forall|while|do|select|when|return|yield|use|import|begin|cobegin|sync|atomic|in|out|inout|ref|true|false|nil'),
    ('Tact',       '.tact',   'cstyle',    'contract|trait|struct|message|fun|native|get|let|const|if|else|while|until|repeat|return|extends|mutates|virtual|abstract|override|self|init|receive|true|false|null'),
    # --- more // line only ---
    ('Carbon',     '.carbon', 'slashline', 'fn|var|let|class|interface|impl|as|if|else|while|for|in|return|break|continue|match|case|and|or|not|package|import|api|library|Self|true|false'),
    ('Hare',       '.ha',     'slashline', 'fn|let|const|def|type|struct|union|enum|if|else|for|switch|case|match|return|break|continue|use|export|static|nullable|size|true|false|null|void'),
    ('Cue',        '.cue',    'slashline', 'package|import|if|for|in|let|true|false|null|string|int|float|bool|bytes|number'),
    ('Ballerina',  '.bal',    'slashline', 'function|service|resource|remote|public|private|isolated|type|record|object|class|if|else|while|foreach|in|return|check|import|listener|worker|start|true|false'),
    # --- more # line ---
    ('Vyper',      '.vy',     'hash',      'def|return|if|elif|else|for|in|while|pass|break|continue|struct|event|interface|public|private|external|internal|view|pure|payable|nonpayable|assert|raise|log|self|True|False'),
    ('Starlark',   '.bzl',    'hash',      'def|return|if|elif|else|for|in|while|break|continue|pass|load|and|or|not|lambda|True|False|None'),
    ('Nushell',    '.nu',     'hash',      'def|let|mut|const|if|else|for|while|loop|match|return|break|continue|export|use|module|source|do|each|where|true|false|null'),
    ('Nickel',     '.ncl',    'hash',      'let|in|if|then|else|fun|import|match|default|doc|true|false|null'),
    ('Just',       '.just',   'hash',      'alias|set|export|if|else'),
    # --- HCL-style ( # or // line + /* */ ) ---
    ('Jsonnet',    '.jsonnet', 'hcl',      'local|function|if|then|else|for|in|import|importstr|error|assert|super|self|null|true|false'),
    # --- Haskell-style ( -- line + {- -} block ) ---
    ('Dhall',      '.dhall',  'dashbrace', 'let|in|if|then|else|merge|forall|assert|as|using|with|Type|Kind|Sort|Bool|Natural|Text|List|Optional|True|False|None|Some'),
    ('Idris',      '.idr',    'dashbrace', 'module|import|data|record|interface|implementation|where|if|then|else|case|of|let|in|do|total|partial|public|export|private|True|False|Nothing|Just'),
    # --- -- line only ---
    ('Futhark',    '.fut',    'dashline',  'let|in|if|then|else|loop|for|while|do|def|entry|type|module|open|import|val|match|case|true|false'),
    # --- Lean 4 ( -- line + /- -/ block ) ---
    ('Lean',       '.lean',   'lean',      'def|theorem|lemma|example|inductive|structure|class|instance|where|if|then|else|match|with|let|fun|do|by|have|show|from|namespace|open|import|variable|true|false'),
]

# Languages needing a real scanner (nested /* */ block comments); see _scanners.py.
# (ClassName, extension, keywords)
NESTED_LANGUAGES = [
    ('Odin', '.odin', 'package|import|proc|struct|union|enum|map|if|else|for|switch|case|when|return|break|continue|defer|using|in|not_in|cast|transmute|distinct|foreign|true|false|nil'),
    ('V',    '.v',    'module|import|fn|struct|enum|interface|union|type|pub|mut|const|if|else|for|in|match|return|break|continue|defer|go|spawn|or|unsafe|true|false|none'),
    ('Jai',  '.jai',  'if|else|for|while|return|break|continue|struct|enum|union|using|defer|cast|xx|it|inline|no_inline|true|false|null'),
]


def _make_language(class_name: str, ext: str, family: str, keywords_str: str):
    compiled = _build_comment_regex(family)
    kw = keywords_str.split('|') if keywords_str else []

    @classmethod
    def file_extension(cls) -> str:
        return ext

    @classmethod
    def keywords(cls) -> list:
        return list(kw)

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return compiled

    namespace = {
        '__doc__': f"{class_name} ({family} comments, generated).",
        'comment_family': family,
        'file_extension': file_extension,
        'keywords': keywords,
        'comment_regex': comment_regex,
    }
    return type(class_name, (BaseLanguage,), namespace)


def _make_nested_language(class_name: str, ext: str, keywords_str: str):
    kw = keywords_str.split('|') if keywords_str else []

    @classmethod
    def file_extension(cls) -> str:
        return ext

    @classmethod
    def keywords(cls) -> list:
        return list(kw)

    namespace = {
        '__doc__': f"{class_name} (nested C-style comments, generated).",
        'comment_family': 'nested',
        'file_extension': file_extension,
        'keywords': keywords,
    }
    return type(class_name, (NestedCStyleLanguage,), namespace)


# Generate, register, and expose each language at module scope.
for _name, _ext, _family, _kw in LANGUAGES:
    _cls = LanguageRegistry.register(_make_language(_name, _ext, _family, _kw))
    globals()[_name] = _cls

for _name, _ext, _kw in NESTED_LANGUAGES:
    _cls = LanguageRegistry.register(_make_nested_language(_name, _ext, _kw))
    globals()[_name] = _cls

del _name, _ext, _family, _kw, _cls
