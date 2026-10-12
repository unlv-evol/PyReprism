"""Reporters for a :class:`PyReprism.clones.CloneReport`.

One report model, several outputs. Every clone---``exact`` (Type-1/2 located
fragments), ``near`` (Type-3 file-level), or ``semantic`` (Type-4)---is rendered
by the same reporters, each kind getting a distinct rule id so CI tooling (e.g.
GitHub code scanning via SARIF) can treat lexical and semantic duplication
separately.
"""
import html
import json
import os
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from .clones import CloneReport

_RULES = {
    'exact': ('pyreprism/exact-clone', 'Duplicated code (Type-1/2)'),
    'near': ('pyreprism/near-clone', 'Near-duplicate file (Type-3)'),
    'semantic': ('pyreprism/semantic-clone', 'Semantic clone (Type-4)'),
}
_KIND_LABEL = {'exact': 'exact (T1/2)', 'near': 'near (T3)',
               'semantic': 'semantic (T4)'}
# Display metadata for the HTML report: (heading, taxonomy tier).
_KIND_META = {'exact': ('Exact', 'T1/2'), 'near': ('Near', 'T3'),
              'semantic': ('Semantic', 'T4')}


def to_json(report: "CloneReport", indent: int = 2) -> str:
    """Structured JSON: summary + every clone with located line ranges."""
    return json.dumps({
        'summary': report.summary(),
        'clones': [c.as_dict() for c in report.clones],
    }, indent=indent)


def to_sarif(report: "CloneReport") -> str:
    """SARIF 2.1.0 for CI / GitHub code scanning. Each clone is a result; the
    partner fragment is a related location."""
    used = sorted({c.kind for c in report.clones})
    rules = [{'id': _RULES[k][0], 'name': _RULES[k][0].split('/')[-1],
              'shortDescription': {'text': _RULES[k][1]}} for k in used]
    results = []
    for c in report.clones:
        rule_id, _desc = _RULES[c.kind]
        results.append({
            'ruleId': rule_id,
            'level': 'warning',
            'message': {'text':
                        f"{_KIND_LABEL[c.kind]} clone: "
                        f"{c.a.path}:{c.a.start_line}-{c.a.end_line} duplicates "
                        f"{c.b.path}:{c.b.start_line}-{c.b.end_line} "
                        f"(score {c.score:.2f})"},
            'locations': [_sarif_loc(c.a)],
            'relatedLocations': [_sarif_loc(c.b, rel_id=1)],
        })
    return json.dumps({
        'version': '2.1.0',
        '$schema': 'https://json.schemastore.org/sarif-2.1.0.json',
        'runs': [{
            'tool': {'driver': {'name': 'PyReprism',
                                'informationUri': 'https://github.com/unlv-evol/PyReprism',
                                'rules': rules}},
            'results': results,
        }],
    }, indent=2)


def _sarif_loc(frag, rel_id=None):
    loc = {'physicalLocation': {
        'artifactLocation': {'uri': frag.path},
        'region': {'startLine': frag.start_line, 'endLine': frag.end_line}}}
    if rel_id is not None:
        loc['id'] = rel_id
    return loc


def to_markdown(report: "CloneReport") -> str:
    """A Markdown summary table plus clones grouped by kind (for PR comments)."""
    s = report.summary()
    lines = ['## PyReprism clone report', '',
             f"- **Files:** {s['files']}",
             f"- **Clones:** {s['clones']}  "
             f"({', '.join(f'{k}: {v}' for k, v in s['by_kind'].items()) or 'none'})",
             f"- **Duplicated lines:** {s['duplicated_lines']} / {s['total_lines']} "
             f"(**{s['duplication_pct']}%**)", '']
    if report.clones:
        lines += ['| Kind | A | B | Score |', '|---|---|---|---|']
        for c in report.clones:
            lines.append(
                f"| {_KIND_LABEL[c.kind]} "
                f"| `{c.a.path}`:{c.a.start_line}-{c.a.end_line} "
                f"| `{c.b.path}`:{c.b.start_line}-{c.b.end_line} "
                f"| {c.score:.2f} |")
    return '\n'.join(lines) + '\n'


def to_console(report: "CloneReport") -> str:
    """Plain human-readable text."""
    s = report.summary()
    out = []
    for c in report.clones:
        out.append(f"[{_KIND_LABEL[c.kind]:<13}] "
                   f"{c.a.path}:{c.a.start_line}-{c.a.end_line}  <->  "
                   f"{c.b.path}:{c.b.start_line}-{c.b.end_line}  "
                   f"(score {c.score:.2f})")
    kinds = ', '.join(f'{k}: {v}' for k, v in s['by_kind'].items()) or 'none'
    out.append(f"\n{s['clones']} clones ({kinds}) across {s['files']} files; "
               f"{s['duplication_pct']}% duplicated lines "
               f"({s['duplicated_lines']}/{s['total_lines']}).")
    return '\n'.join(out)


# --------------------------------------------------------------------- HTML
_HTML_CSS = """
:root{--bg:#FBFCFE;--surface:#fff;--surface-2:#F3F6FA;--inset:#EEF2F7;
--ink:#182233;--muted:#5A6675;--faint:#8794A6;--border:#E4E9F0;--border-strong:#D3DCE6;
--brand:#C9761B;--brand-ink:#9A5A12;--exact:#2E5E9E;--exact-soft:#E9F0FA;
--near:#0C8079;--near-soft:#DEF2F0;--semantic:#7A4FC0;--semantic-soft:#EEE7F8;
--ok:#1E9E6A;--ok-soft:#E1F4EB;--warn:#C0821A;--crit:#CF4141;--crit-soft:#FBE7E7;
--shadow:0 1px 2px rgba(24,34,51,.06),0 6px 20px -12px rgba(24,34,51,.18);--radius:12px}
:root:not([data-theme=light]){@media(prefers-color-scheme:dark){
--bg:#0E141C;--surface:#141C26;--surface-2:#1A2430;--inset:#10171F;--ink:#E7ECF3;
--muted:#9DA9B8;--faint:#697687;--border:#24303E;--border-strong:#32404F;
--brand:#F0A24E;--brand-ink:#F3B472;--exact:#7AA6E4;--exact-soft:#15263A;
--near:#46C6BF;--near-soft:#103130;--semantic:#B79BE9;--semantic-soft:#241B37;
--ok:#43C089;--ok-soft:#10251C;--warn:#E1AC4E;--crit:#E86E6E;--crit-soft:#2C1616;
--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -14px rgba(0,0,0,.6)}}
:root[data-theme=dark]{--bg:#0E141C;--surface:#141C26;--surface-2:#1A2430;--inset:#10171F;
--ink:#E7ECF3;--muted:#9DA9B8;--faint:#697687;--border:#24303E;--border-strong:#32404F;
--brand:#F0A24E;--brand-ink:#F3B472;--exact:#7AA6E4;--exact-soft:#15263A;
--near:#46C6BF;--near-soft:#103130;--semantic:#B79BE9;--semantic-soft:#241B37;
--ok:#43C089;--ok-soft:#10251C;--warn:#E1AC4E;--crit:#E86E6E;--crit-soft:#2C1616;
--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -14px rgba(0,0,0,.6)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;
font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased}
.mono{font-family:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;font-variant-ligatures:none}
.tnum{font-variant-numeric:tabular-nums}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
header{border-bottom:1px solid var(--border);background:var(--surface);position:sticky;top:0;z-index:20}
.head-row{display:flex;align-items:center;gap:16px;padding:14px 0;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px}
.mark{width:30px;height:30px;border-radius:8px;flex:none;background:linear-gradient(150deg,var(--brand),#d1462a);
display:grid;place-items:center;color:#fff;font-weight:700;font-family:"JetBrains Mono",monospace;font-size:14px}
.brand b{font-weight:600;font-size:15.5px}.brand .sub{color:var(--faint);font-weight:500}
.target{color:var(--muted);font-size:13px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.target .repo{color:var(--ink);font-weight:500}
.dot{width:3px;height:3px;border-radius:50%;background:var(--border-strong)}
.spacer{flex:1 1 20px}
.icon-btn{width:34px;height:34px;flex:none;border-radius:8px;cursor:pointer;border:1px solid var(--border);
background:var(--surface);color:var(--muted);display:grid;place-items:center;font-size:15px}
.icon-btn:hover{border-color:var(--border-strong);color:var(--ink)}
.summary{padding:26px 0 10px}
.eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:11px;font-weight:600;color:var(--faint)}
.sum-grid{display:grid;gap:16px;margin-top:12px;grid-template-columns:1.35fr 1fr}
@media(max-width:760px){.sum-grid{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow)}
.dup-card{padding:20px 22px;display:flex;flex-direction:column;gap:14px}
.dup-head{display:flex;align-items:baseline;gap:12px}
.dup-num{font-size:42px;font-weight:600;letter-spacing:-.02em;line-height:1}
.gate{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:600;padding:5px 10px;border-radius:999px}
.gate.fail{background:var(--crit-soft);color:var(--crit)}.gate.pass{background:var(--ok-soft);color:var(--ok)}
.gate .pulse{width:7px;height:7px;border-radius:50%;background:currentColor}
.dup-sub{color:var(--muted);font-size:13px}.dup-sub b{color:var(--ink);font-weight:600}
.meter{position:relative}
.meter-track{height:12px;border-radius:999px;background:var(--inset);overflow:hidden;border:1px solid var(--border)}
.meter-fill{height:100%;display:flex}.meter-ok{background:var(--warn)}.meter-over{background:var(--crit)}
.meter-one{background:var(--ok);height:100%}
.meter-scale{display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:var(--faint)}
.threshold{position:absolute;top:-4px;bottom:15px;width:0;border-left:2px dashed var(--crit)}
.threshold span{position:absolute;top:-17px;left:50%;transform:translateX(-50%);font-size:10.5px;font-weight:600;color:var(--crit);white-space:nowrap}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tile{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;box-shadow:var(--shadow)}
.tile .k{font-size:12px;color:var(--muted);font-weight:500}
.tile .v{font-size:22px;font-weight:600;margin-top:4px}
.kinds{grid-column:1/-1;display:flex;gap:10px;flex-wrap:wrap}
.kpill{display:inline-flex;align-items:center;gap:8px;padding:8px 13px;border-radius:10px;font-size:13px;
font-weight:500;flex:1;border:1px solid var(--border);background:var(--surface);min-width:130px}
.kpill .swatch{width:9px;height:9px;border-radius:3px;flex:none}
.kpill .n{margin-left:auto;font-weight:700;font-family:"JetBrains Mono",monospace}
.kpill .lab{color:var(--muted)}
.kpill.exact{border-left:3px solid var(--exact)}.kpill.exact .swatch{background:var(--exact)}
.kpill.near{border-left:3px solid var(--near)}.kpill.near .swatch{background:var(--near)}
.kpill.semantic{border-left:3px solid var(--semantic)}.kpill.semantic .swatch{background:var(--semantic)}
.toolbar{display:flex;align-items:center;gap:8px;margin:26px 0 14px;flex-wrap:wrap}
.tabs{display:flex;gap:4px;background:var(--inset);padding:4px;border-radius:10px;border:1px solid var(--border)}
.tab{border:0;background:transparent;cursor:pointer;color:var(--muted);font:inherit;font-weight:500;font-size:13px;
padding:6px 12px;border-radius:7px;display:inline-flex;align-items:center;gap:7px}
.tab .c{font-family:"JetBrains Mono",monospace;font-size:11.5px;color:var(--faint)}
.tab[aria-selected=true]{background:var(--surface);color:var(--ink);box-shadow:var(--shadow)}
.tab[aria-selected=true] .c{color:var(--brand-ink)}
.toolbar .note{margin-left:auto;font-size:12.5px;color:var(--faint)}
.list{display:flex;flex-direction:column;gap:12px;padding-bottom:8px}
.empty{color:var(--muted);padding:28px;text-align:center;border:1px dashed var(--border);border-radius:var(--radius)}
.clone{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
.clone.exact{border-left:3px solid var(--exact)}.clone.near{border-left:3px solid var(--near)}
.clone.semantic{border-left:3px solid var(--semantic)}
.clone-head{display:flex;align-items:center;gap:12px;padding:12px 16px;flex-wrap:wrap}
.badge{display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:700;letter-spacing:.04em;
text-transform:uppercase;padding:4px 9px;border-radius:6px}
.exact .badge{background:var(--exact-soft);color:var(--exact)}.near .badge{background:var(--near-soft);color:var(--near)}
.semantic .badge{background:var(--semantic-soft);color:var(--semantic)}
.badge .sw{width:8px;height:8px;border-radius:2px;background:currentColor}
.rule{font-size:12px;color:var(--faint)}
.clone-head .meta{margin-left:auto;display:flex;align-items:center;gap:14px;color:var(--muted);font-size:12.5px}
.clone-head .meta .score{color:var(--ink);font-weight:600}
.lang{font-size:11px;padding:2px 7px;border-radius:5px;background:var(--inset);border:1px solid var(--border);color:var(--muted)}
.frags{padding:0 16px 14px;display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center}
@media(max-width:640px){.frags{grid-template-columns:1fr}.arrow{transform:rotate(90deg);justify-self:center}}
.frag{background:var(--inset);border:1px solid var(--border);border-radius:9px;padding:9px 12px;min-width:0}
.frag .path{font-size:13px;overflow-x:auto;white-space:nowrap}.frag .path b{color:var(--ink);font-weight:500}
.frag .path .dir{color:var(--faint)}
.frag .loc{font-size:12px;color:var(--muted);margin-top:2px}.frag .loc .range{color:var(--brand-ink);font-weight:500}
.arrow{color:var(--faint);font-size:16px}
details.view{border-top:1px solid var(--border)}
details.view>summary{cursor:pointer;padding:10px 16px;font-size:12.5px;font-weight:500;color:var(--muted);
list-style:none;user-select:none}
details.view>summary::-webkit-details-marker{display:none}
details.view>summary:before{content:"\\25B8  ";color:var(--faint)}
details.view[open]>summary:before{content:"\\25BE  "}
details.view>summary:hover{color:var(--ink)}
.diff{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);border-top:1px solid var(--border)}
@media(max-width:640px){.diff{grid-template-columns:1fr}}
.code{background:var(--surface-2);overflow-x:auto;padding:10px 0}
.code .fname{font-size:11.5px;color:var(--faint);padding:0 14px 8px}
.code pre{margin:0;font-family:"JetBrains Mono",monospace;font-size:12.5px;line-height:1.65}
.code .ln{display:block;padding:0 14px;white-space:pre}
.code .ln .g{color:var(--faint);display:inline-block;min-width:34px;text-align:right;margin-right:12px;user-select:none}
.code .ln.hl{background:color-mix(in srgb,var(--exact) 12%,transparent);box-shadow:inset 2px 0 0 var(--exact)}
.semantic .code .ln.hl{background:color-mix(in srgb,var(--semantic) 12%,transparent);box-shadow:inset 2px 0 0 var(--semantic)}
.note{padding:12px 16px;font-size:12.5px;color:var(--muted);border-top:1px solid var(--border);background:var(--surface-2)}
footer{border-top:1px solid var(--border);margin-top:26px;padding:20px 0 40px;color:var(--muted);font-size:12.5px}
.hidden{display:none!important}
"""

_HTML_JS = """
(function(){var r=document.documentElement,b=document.getElementById('theme');
try{var s=localStorage.getItem('pr-theme');if(s)r.setAttribute('data-theme',s);}catch(e){}
if(b)b.addEventListener('click',function(){var c=r.getAttribute('data-theme');
if(!c)c=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
var n=c==='dark'?'light':'dark';r.setAttribute('data-theme',n);
try{localStorage.setItem('pr-theme',n);}catch(e){}});
var t=[].slice.call(document.querySelectorAll('.tab')),
c=[].slice.call(document.querySelectorAll('.clone'));
t.forEach(function(x){x.addEventListener('click',function(){
t.forEach(function(y){y.setAttribute('aria-selected',y===x?'true':'false');});
var f=x.getAttribute('data-filter');
c.forEach(function(el){el.classList.toggle('hidden',f!=='all'&&el.getAttribute('data-kind')!==f);});});});})();
"""

_ARROW = '&#8646;'  # rightwards-over-leftwards arrow


def _lang_label(path: str) -> str:
    ext = os.path.splitext(path)[1].lstrip('.')
    return ext.upper() if ext else 'text'


def _path_html(path: str) -> str:
    head, tail = os.path.split(path)
    e = html.escape
    dir_html = f'<span class="dir">{e(head)}/</span>' if head else ''
    return f'{dir_html}<b>{e(tail or path)}</b>'


def _frag_html(frag) -> str:
    span = (f'lines <span class="range">{frag.start_line}&ndash;{frag.end_line}</span>'
            if frag.end_line != frag.start_line
            else f'line <span class="range">{frag.start_line}</span>')
    return (f'<div class="frag"><div class="path mono">{_path_html(frag.path)}</div>'
            f'<div class="loc mono">{span}</div></div>')


def _snippet_html(frag, sources: Dict[str, Optional[List[str]]], max_lines: int) -> str:
    lines = sources.get(frag.path)
    if lines is None:
        return ''
    start, end = frag.start_line, min(frag.end_line, frag.start_line + max_lines - 1)
    rows = []
    for n in range(start, end + 1):
        if n - 1 >= len(lines):
            break
        rows.append(f'<span class="ln hl"><span class="g">{n}</span>'
                    f'{html.escape(lines[n - 1])}</span>')
    if frag.end_line > end:
        rows.append('<span class="ln"><span class="g">&hellip;</span></span>')
    body = ''.join(rows)
    return (f'<div class="code"><div class="fname mono">{html.escape(os.path.basename(frag.path))}</div>'
            f'<pre>{body}</pre></div>')


def _clone_html(clone, sources: Optional[Dict[str, Optional[List[str]]]],
                max_lines: int) -> str:
    heading, tier = _KIND_META.get(clone.kind, (clone.kind.title(), ''))
    rule_id = _RULES[clone.kind][0]
    size = (f'{clone.tokens} tokens &middot; {clone.a.lines} lines' if clone.tokens
            else f'{clone.a.lines} lines')
    head = (f'<div class="clone-head">'
            f'<span class="badge"><span class="sw"></span>{heading}</span>'
            f'<span class="rule mono">{rule_id}</span>'
            f'<span class="meta"><span class="lang">{html.escape(_lang_label(clone.a.path))}</span>'
            f'<span class="mono">{size}</span>'
            f'<span class="score mono">{clone.score:.2f}</span></span></div>')
    frags = (f'<div class="frags">{_frag_html(clone.a)}'
             f'<div class="arrow">{_ARROW}</div>{_frag_html(clone.b)}</div>')
    view = ''
    if sources is not None:
        sa = _snippet_html(clone.a, sources, max_lines)
        sb = _snippet_html(clone.b, sources, max_lines)
        if sa and sb:
            view = (f'<details class="view"><summary>View fragments '
                    f'(tier {tier})</summary><div class="diff">{sa}{sb}</div></details>')
    return f'<article class="clone {clone.kind}" data-kind="{clone.kind}">{head}{frags}{view}</article>'


def to_html(report: "CloneReport", *, title: str = 'PyReprism Clone Report',
            target: Optional[str] = None, max_duplication: Optional[float] = None,
            embed_source: bool = True, max_snippet_lines: int = 40) -> str:
    """A self-contained, theme-aware HTML clone report.

    Renders the summary (duplication meter, optional ``max_duplication`` CI gate,
    per-kind counts) and every clone as a card with its located line ranges, score,
    and SARIF rule id. When ``embed_source`` is set, exact and function-level clones
    also show a side-by-side snippet read from disk (missing files are skipped).
    Pure ``report`` in, ``str`` of HTML out; no external assets.
    """
    s = report.summary()
    pct = s['duplication_pct']
    by_kind = s['by_kind']
    e = html.escape

    # source cache for snippets
    sources: Optional[Dict[str, Optional[List[str]]]] = None
    if embed_source:
        sources = {}
        for c in report.clones:
            for frag in (c.a, c.b):
                if frag.path not in sources:
                    try:
                        with open(frag.path, encoding='utf-8', errors='replace') as fh:
                            sources[frag.path] = fh.read().split('\n')
                    except OSError:
                        sources[frag.path] = None

    # gate
    gate = ''
    if max_duplication is not None:
        failed = pct > max_duplication
        cls, word = ('fail', 'FAILED') if failed else ('pass', 'PASSED')
        gate = f'<div class="gate {cls}"><span class="pulse"></span>CI&nbsp;{word}</div>'
        gate_sub = (f' &mdash; {"over" if failed else "within"} the '
                    f'<b>{max_duplication:g}%</b> gate')
    else:
        gate_sub = ''

    # meter
    scale = max(10.0, pct * 1.3, (max_duplication or 0) * 1.6)
    if max_duplication is not None:
        thr = max_duplication
        ok_w = min(pct, thr) / scale * 100
        over_w = max(0.0, pct - thr) / scale * 100
        fill = (f'<div class="meter-ok" style="width:{ok_w:.1f}%"></div>'
                f'<div class="meter-over" style="width:{over_w:.1f}%"></div>')
        marker = f'<div class="threshold" style="left:{thr / scale * 100:.1f}%"><span>{thr:g}% gate</span></div>'
    else:
        color = 'var(--ok)' if pct < 3 else ('var(--warn)' if pct < 10 else 'var(--crit)')
        fill = f'<div class="meter-one" style="width:{pct / scale * 100:.1f}%;background:{color}"></div>'
        marker = ''

    kpills = ''
    for kind, (heading, tier) in _KIND_META.items():
        n = by_kind.get(kind, 0)
        kpills += (f'<span class="kpill {kind}"><span class="swatch"></span>'
                   f'<span class="lab">{heading} <span class="mono" style="font-size:11px">{tier}</span></span>'
                   f'<span class="n">{n}</span></span>')

    tabs = f'<button class="tab" role="tab" aria-selected="true" data-filter="all">All <span class="c">{s["clones"]}</span></button>'
    for kind, (heading, _tier) in _KIND_META.items():
        if by_kind.get(kind):
            tabs += (f'<button class="tab" role="tab" aria-selected="false" data-filter="{kind}">'
                     f'{heading} <span class="c">{by_kind[kind]}</span></button>')

    if report.clones:
        cards = ''.join(_clone_html(c, sources, max_snippet_lines) for c in report.clones)
    else:
        cards = '<div class="empty">No clones detected.</div>'

    header_target = (f'<div class="target"><span class="repo mono">{e(target)}</span>'
                     f'<span class="dot"></span><span>{s["files"]} files</span></div>'
                     if target else
                     f'<div class="target"><span>{s["files"]} files scanned</span></div>')

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
<style>{_HTML_CSS}</style>
</head>
<body>
<header><div class="wrap head-row">
<div class="brand"><span class="mark">P&lt;&gt;</span><span><b>PyReprism</b> <span class="sub mono">clones</span></span></div>
{header_target}
<span class="spacer"></span>
<button class="icon-btn" id="theme" aria-label="Toggle theme">&#9788;</button>
</div></header>
<main class="wrap">
<section class="summary">
<div class="eyebrow">Duplication report</div>
<div class="sum-grid">
<div class="card dup-card">
<div class="dup-head"><div class="dup-num tnum">{pct:g}<span style="font-size:22px;color:var(--muted)">%</span></div>{gate}</div>
<div class="dup-sub"><b>{s['duplicated_lines']:,}</b> of {s['total_lines']:,} lines duplicated{gate_sub}.</div>
<div class="meter"><div class="meter-track"><div class="meter-fill">{fill}</div></div>{marker}
<div class="meter-scale mono"><span>0%</span><span>duplicated lines</span><span>{scale:g}%</span></div></div>
</div>
<div class="tiles">
<div class="tile"><div class="k">Files scanned</div><div class="v tnum">{s['files']:,}</div></div>
<div class="tile"><div class="k">Clone pairs</div><div class="v tnum">{s['clones']:,}</div></div>
<div class="kinds">{kpills}</div>
</div>
</div>
</section>
<div class="toolbar"><div class="tabs" role="tablist" aria-label="Filter by clone type">{tabs}</div>
<span class="note">located over the normalized token stream</span></div>
<div class="list">{cards}</div>
</main>
<footer class="wrap">Generated by PyReprism &middot; fidelity ladder: lexical &rarr; semantic</footer>
<script>{_HTML_JS}</script>
</body>
</html>
'''


REPORTERS = {'json': to_json, 'sarif': to_sarif, 'markdown': to_markdown,
             'console': to_console, 'html': to_html}


def render(report: "CloneReport", fmt: str = 'console') -> str:
    """Render ``report`` in the named format (``console`` default)."""
    try:
        return REPORTERS[fmt](report)
    except KeyError:
        raise ValueError(f"unknown reporter {fmt!r}; choose from {sorted(REPORTERS)}")
