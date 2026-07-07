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

from . import __version__, _tokenops, detect_language, get_language, preprocess
from .engines import get_engine
from .tokens import TokenType

CONSTRUCTS = ['comments', 'keywords', 'numbers', 'operators', 'strings', 'identifiers']
_CONSTRUCT_TYPE = {
    'comments': TokenType.COMMENT, 'keywords': TokenType.KEYWORD,
    'numbers': TokenType.NUMBER, 'operators': TokenType.OPERATOR,
    'strings': TokenType.STRING, 'identifiers': TokenType.IDENTIFIER,
}


def _iter_inputs(paths: List[str]):
    """Yield ``(label, text, filename, base)`` for each input.

    ``filename`` and ``base`` are None for stdin. Directories are walked for
    supported source files (``base`` is the directory, for output mirroring).
    """
    import os

    from .batch import iter_source_files

    if not paths:
        yield ('<stdin>', sys.stdin.read(), None, None)
        return
    for pattern in paths:
        if os.path.isdir(pattern):
            for base, path, _cls in iter_source_files(pattern):
                try:
                    yield (str(path), path.read_text(encoding='utf-8', errors='replace'),
                           str(path), str(base))
                except OSError as exc:
                    print(f"pyreprism: {exc}", file=sys.stderr)
            continue
        matches = glob.glob(pattern, recursive=True) if any(c in pattern for c in '*?[') else [pattern]
        if not matches:
            print(f"pyreprism: no such file: {pattern}", file=sys.stderr)
            continue
        for filepath in matches:
            if os.path.isdir(filepath):
                continue
            try:
                with open(filepath, 'r', encoding='utf-8') as handle:
                    yield (filepath, handle.read(), filepath, None)
            except OSError as exc:
                print(f"pyreprism: {exc}", file=sys.stderr)


def _resolve(lang: Optional[str], filename: Optional[str], source: Optional[str] = None):
    if lang:
        return get_language(lang)
    if filename:
        cls = detect_language(filename=filename)
        if cls:
            return cls
    if source is not None:
        cls = detect_language(source=source)
        if cls:
            return cls
    print("pyreprism: could not determine language; pass --lang", file=sys.stderr)
    raise SystemExit(2)


def _multiple(paths) -> bool:
    """True when the inputs are expected to expand to more than one file."""
    import os
    return len(paths) > 1 or any(os.path.isdir(p) for p in paths)


def _op(cls, action: str, construct: str, text: str, engine: str):
    """Run remove/extract/count for a construct via the selected engine."""
    if engine in (None, 'regex'):
        fn = getattr(cls, f'{action}_{construct}', None)
        if fn is None:
            raise SystemExit(f"pyreprism: '{action} {construct}' is not supported")
        return fn(text)
    tokens = get_engine(engine).tokenize(text, cls)
    return getattr(_tokenops, action)(tokens, _CONSTRUCT_TYPE[construct])


def _cmd_remove(args) -> int:
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        result = _op(cls, 'remove', args.construct, text, args.engine)
        _emit(result, filename, base, args)
    return 0


def _cmd_preprocess(args) -> int:
    steps = [s.strip() for s in args.steps.split(',') if s.strip()]
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        result = preprocess(text, lang=cls, steps=steps, engine=args.engine)
        _emit(result, filename, base, args)
    return 0


def _cmd_extract(args) -> int:
    multiple = _multiple(args.paths)
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        items = _op(cls, 'extract', args.construct, text, args.engine)
        if args.json:
            print(json.dumps({label: items} if multiple else items))
        else:
            if multiple:
                print(f"==> {label} <==")
            for item in items:
                print(item)
    return 0


def _cmd_count(args) -> int:
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        count = _op(cls, 'count', args.construct, text, args.engine)
        print(f"{count}\t{label}" if _multiple(args.paths) else count)
    return 0


def _cmd_tokenize(args) -> int:
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        tokens = get_engine(args.engine).tokenize(text, cls)
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
    multiple = _multiple(args.paths)
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        if args.engine in (None, 'regex'):
            data = cls.stats(text).as_dict()
        else:
            data = _tokenops.stats(get_engine(args.engine).tokenize(text, cls), text).as_dict()
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
    for label, text, filename, base in _iter_inputs(args.paths):
        cls = _resolve(args.lang, filename, text)
        if args.engine in (None, 'regex'):
            result = cls.normalize(text, **options)
        else:
            result = _tokenops.normalize(get_engine(args.engine).tokenize(text, cls), **options)
        _emit(result, filename, base, args)
    return 0


def _cmd_scan(args) -> int:
    from .batch import analyze

    report = analyze(args.paths, engine=args.engine, recursive=not args.no_recursive,
                     include=args.include, exclude=args.exclude)
    if args.json:
        print(report.to_json())
        return 0
    if args.csv:
        print(report.to_csv(), end='')
        return 0

    if args.per_file:
        for f in report.ok:
            print(f"{f.path}\t{f.language}\t{f.stats.code_lines} code, "
                  f"{f.stats.comment_lines} comment")
        print()
    by_lang = report.by_language()
    if by_lang:
        width = max(len(name) for name in by_lang)
        print(f"{'language'.ljust(width)}  files  code  comment  blank")
        for name, agg in by_lang.items():
            print(f"{name.ljust(width)}  {agg['files']:>5}  {agg['code_lines']:>4}  "
                  f"{agg['comment_lines']:>7}  {agg['blank_lines']:>5}")
    totals = report.totals()
    print(f"\n{totals['files']} files, {totals['lines']} lines "
          f"({totals['code_lines']} code, {totals['comment_lines']} comment, "
          f"{totals['blank_lines']} blank)")
    if report.errors:
        print(f"{len(report.errors)} file(s) could not be processed", file=sys.stderr)
    return 0


def _cmd_diff(args) -> int:
    from .diffs import cosmetic_files, diff_stats, parse

    if args.paths:
        texts = []
        for path in args.paths:
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as handle:
                    texts.append(handle.read())
            except OSError as exc:
                print(f"pyreprism: {exc}", file=sys.stderr)
        diff = parse('\n'.join(texts))
    else:
        diff = parse(sys.stdin.read())

    if args.cosmetic:
        for f in cosmetic_files(diff):
            print(f.path)
        return 0

    report = diff_stats(diff)
    if args.json:
        print(report.to_json())
        return 0
    if args.csv:
        print(report.to_csv(), end='')
        return 0

    if args.per_file:
        for f in report.files:
            tag = ' [binary]' if f.is_binary else ''
            print(f"{f.path}\t{f.language}\t+{f.added_code}/-{f.removed_code} code, "
                  f"+{f.added_comment}/-{f.removed_comment} comment{tag}")
        print()
    totals = report.totals()
    print(f"{totals['files']} files: "
          f"+{totals['added_code']}/-{totals['removed_code']} code, "
          f"+{totals['added_comment']}/-{totals['removed_comment']} comment, "
          f"+{totals['added_blank']}/-{totals['removed_blank']} blank")
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


def _emit(result: str, filename: Optional[str], base: Optional[str], args) -> None:
    import os

    output = getattr(args, 'output', None)
    if output and filename:
        src = os.path.abspath(filename)
        if base and os.path.isdir(base):
            rel = os.path.relpath(src, os.path.abspath(base))
        else:
            rel = os.path.basename(src)
        dest = os.path.join(output, rel)
        os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as handle:
            handle.write(result)
    elif getattr(args, 'in_place', False) and filename:
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
            p.add_argument('-e', '--engine', default='regex',
                           choices=['regex', 'pygments', 'auto'],
                           help="tokenization backend (default: regex; 'pygments' is more "
                                "accurate but needs pyreprism[accurate])")

    def add_output(p):
        p.add_argument('-i', '--in-place', action='store_true',
                       help='rewrite files in place instead of printing to stdout')
        p.add_argument('-o', '--output', metavar='DIR',
                       help='write results into DIR, mirroring the input tree')

    p_remove = sub.add_parser('remove', help='remove a construct from the source')
    p_remove.add_argument('construct', choices=[c for c in CONSTRUCTS if c != 'identifiers'])
    add_common(p_remove)
    add_output(p_remove)
    p_remove.set_defaults(func=_cmd_remove)

    p_pre = sub.add_parser('preprocess', help='apply a sequence of removal steps')
    p_pre.add_argument('-s', '--steps', default='comments',
                       help='comma-separated steps: comments,strings,numbers,operators,'
                            'keywords,whitespace')
    add_common(p_pre)
    add_output(p_pre)
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
    add_output(p_norm)
    p_norm.set_defaults(func=_cmd_normalize)

    p_scan = sub.add_parser('scan',
                            help='walk directories and report aggregate metrics')
    p_scan.add_argument('paths', nargs='+', help='directories or files to scan')
    p_scan.add_argument('-e', '--engine', default='regex',
                        choices=['regex', 'pygments', 'auto'])
    p_scan.add_argument('--json', action='store_true', help='emit the full JSON report')
    p_scan.add_argument('--csv', action='store_true', help='emit per-file CSV')
    p_scan.add_argument('--per-file', action='store_true',
                        help='include a per-file breakdown in the text report')
    p_scan.add_argument('--include', action='append', metavar='GLOB',
                        help='only include files matching GLOB (repeatable)')
    p_scan.add_argument('--exclude', action='append', metavar='GLOB',
                        help='skip files matching GLOB (repeatable)')
    p_scan.add_argument('--no-recursive', action='store_true',
                        help='do not descend into subdirectories')
    p_scan.set_defaults(func=_cmd_scan)

    p_diff = sub.add_parser('diff',
                            help='analyze a unified/git diff (churn metrics, cosmetic detection)')
    p_diff.add_argument('paths', nargs='*', help='diff files (default: read stdin)')
    p_diff.add_argument('--json', action='store_true', help='emit the full JSON report')
    p_diff.add_argument('--csv', action='store_true', help='emit per-file CSV')
    p_diff.add_argument('--per-file', action='store_true',
                        help='include a per-file breakdown in the text report')
    p_diff.add_argument('--cosmetic', action='store_true',
                        help='list only files whose change is comment/whitespace-only')
    p_diff.set_defaults(func=_cmd_diff)

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
