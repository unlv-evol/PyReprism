"""Command-line interface for PyReprism.

Usage examples::

    pyreprism remove comments file.py
    cat file.go | pyreprism remove comments --lang go
    pyreprism extract comments src/**/*.py
    pyreprism count comments --lang python file.py
    pyreprism preprocess --steps comments,strings,whitespace file.java
    pyreprism tokenize --json file.py
    pyreprism languages
"""
import argparse
import glob
import json
import sys
from typing import List, Optional

from . import __version__, detect_language, get_language, preprocess

CONSTRUCTS = ['comments', 'keywords', 'numbers', 'operators', 'strings', 'identifiers']


def _iter_inputs(paths: List[str]):
    """Yield ``(label, text, filename)`` for each input; filename is None for stdin."""
    if not paths:
        yield ('<stdin>', sys.stdin.read(), None)
        return
    for pattern in paths:
        matches = glob.glob(pattern, recursive=True) if any(c in pattern for c in '*?[') else [pattern]
        if not matches:
            print(f"pyreprism: no such file: {pattern}", file=sys.stderr)
            continue
        for filepath in matches:
            try:
                with open(filepath, 'r', encoding='utf-8') as handle:
                    yield (filepath, handle.read(), filepath)
            except OSError as exc:
                print(f"pyreprism: {exc}", file=sys.stderr)


def _resolve(lang: Optional[str], filename: Optional[str]):
    if lang:
        return get_language(lang)
    if filename:
        cls = detect_language(filename=filename)
        if cls:
            return cls
    print("pyreprism: could not determine language; pass --lang", file=sys.stderr)
    raise SystemExit(2)


def _method(cls, action: str, construct: str):
    fn = getattr(cls, f'{action}_{construct}', None)
    if fn is None:
        raise SystemExit(f"pyreprism: '{action} {construct}' is not supported")
    return fn


def _cmd_remove(args) -> int:
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        result = _method(cls, 'remove', args.construct)(text)
        _emit(result, filename, args.in_place, args)
    return 0


def _cmd_preprocess(args) -> int:
    steps = [s.strip() for s in args.steps.split(',') if s.strip()]
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        result = preprocess(text, lang=cls, steps=steps)
        _emit(result, filename, args.in_place, args)
    return 0


def _cmd_extract(args) -> int:
    multiple = len(args.paths) > 1
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        items = _method(cls, 'extract', args.construct)(text)
        if args.json:
            print(json.dumps({label: items} if multiple else items))
        else:
            if multiple:
                print(f"==> {label} <==")
            for item in items:
                print(item)
    return 0


def _cmd_count(args) -> int:
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        count = _method(cls, 'count', args.construct)(text)
        print(f"{count}\t{label}" if len(args.paths) > 1 else count)
    return 0


def _cmd_tokenize(args) -> int:
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        tokens = cls.tokenize(text)
        if args.json:
            print(json.dumps([
                {'type': t.type.value, 'value': t.value,
                 'start': t.start, 'end': t.end, 'line': t.line}
                for t in tokens
            ]))
        else:
            for t in tokens:
                print(f"{t.line}\t{t.type.value}\t{t.value!r}")
    return 0


def _cmd_stats(args) -> int:
    multiple = len(args.paths) > 1
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        data = cls.stats(text).as_dict()
        if args.json:
            print(json.dumps({label: data} if multiple else data))
        else:
            if multiple:
                print(f"==> {label} <==")
            width = max(len(k) for k in data)
            for key, value in data.items():
                print(f"{key.ljust(width)}  {value}")
    return 0


def _cmd_normalize(args) -> int:
    options = dict(
        drop_comments=not args.keep_comments,
        mask_numbers=not args.keep_numbers,
        mask_strings=not args.keep_strings,
        rename_identifiers=not args.keep_names,
        collapse_whitespace=args.collapse_whitespace,
    )
    for label, text, filename in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename)
        result = cls.normalize(text, **options)
        _emit(result, filename, args.in_place, args)
    return 0


def _cmd_languages(args) -> int:
    from .languages import _load_all_languages
    from .languages.registry import LanguageRegistry

    _load_all_languages()
    rows = []
    for name, cls in sorted(LanguageRegistry.all().items()):
        try:
            ext = cls.file_extension()
        except Exception:
            ext = '?'
        rows.append((name, ext))
    width = max((len(n) for n, _ in rows), default=0)
    for name, ext in rows:
        print(f"{name.ljust(width)}  {ext}")
    print(f"\n{len(rows)} languages", file=sys.stderr)
    return 0


def _emit(result: str, filename: Optional[str], in_place: bool, args) -> None:
    if in_place and filename:
        with open(filename, 'w', encoding='utf-8') as handle:
            handle.write(result)
    else:
        sys.stdout.write(result)
        if not result.endswith('\n'):
            sys.stdout.write('\n')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pyreprism',
        description='Preprocess source code: strip/extract/count comments, strings, '
                    'numbers, operators, keywords and identifiers across 145+ languages.',
    )
    parser.add_argument('--version', action='version', version=f'pyreprism {__version__}')
    sub = parser.add_subparsers(dest='command', required=True)

    def add_common(p, lang=True):
        p.add_argument('paths', nargs='*', help='files or globs (default: read stdin)')
        if lang:
            p.add_argument('-l', '--lang',
                           help='language name, extension, or class (auto-detected from '
                                'filename when omitted)')

    p_remove = sub.add_parser('remove', help='remove a construct from the source')
    p_remove.add_argument('construct', choices=[c for c in CONSTRUCTS if c != 'identifiers'])
    add_common(p_remove)
    p_remove.add_argument('-i', '--in-place', action='store_true',
                          help='rewrite files in place instead of printing to stdout')
    p_remove.set_defaults(func=_cmd_remove)

    p_pre = sub.add_parser('preprocess', help='apply a sequence of removal steps')
    p_pre.add_argument('-s', '--steps', default='comments',
                       help='comma-separated steps: comments,strings,numbers,operators,'
                            'keywords,whitespace')
    add_common(p_pre)
    p_pre.add_argument('-i', '--in-place', action='store_true')
    p_pre.set_defaults(func=_cmd_preprocess)

    p_extract = sub.add_parser('extract', help='extract occurrences of a construct')
    p_extract.add_argument('construct', choices=CONSTRUCTS)
    add_common(p_extract)
    p_extract.add_argument('--json', action='store_true', help='emit JSON')
    p_extract.set_defaults(func=_cmd_extract)

    p_count = sub.add_parser('count', help='count occurrences of a construct')
    p_count.add_argument('construct', choices=CONSTRUCTS)
    add_common(p_count)
    p_count.set_defaults(func=_cmd_count)

    p_tok = sub.add_parser('tokenize', help='emit the typed token stream')
    add_common(p_tok)
    p_tok.add_argument('--json', action='store_true', help='emit JSON')
    p_tok.set_defaults(func=_cmd_tokenize)

    p_stats = sub.add_parser('stats', help='report line/token metrics')
    add_common(p_stats)
    p_stats.add_argument('--json', action='store_true', help='emit JSON')
    p_stats.set_defaults(func=_cmd_stats)

    p_norm = sub.add_parser('normalize',
                            help='canonicalize code (rename identifiers, mask literals) for ML')
    add_common(p_norm)
    p_norm.add_argument('--keep-comments', action='store_true')
    p_norm.add_argument('--keep-numbers', action='store_true')
    p_norm.add_argument('--keep-strings', action='store_true')
    p_norm.add_argument('--keep-names', action='store_true',
                        help='do not rename identifiers')
    p_norm.add_argument('--collapse-whitespace', action='store_true')
    p_norm.add_argument('-i', '--in-place', action='store_true')
    p_norm.set_defaults(func=_cmd_normalize)

    p_langs = sub.add_parser('languages', help='list supported languages and extensions')
    p_langs.set_defaults(func=_cmd_languages)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else list(argv))
    try:
        return args.func(args)
    except SystemExit:
        raise
    except ValueError as exc:
        print(f"pyreprism: {exc}", file=sys.stderr)
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
