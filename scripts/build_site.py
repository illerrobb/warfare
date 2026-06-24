#!/usr/bin/env python3
from pathlib import Path
import html, re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ORDER = [
    ('AVVERTENZA.md', 'Avvertenza', None),
    ('0.md', 'Introduzione', None),
    ('1.md', 'Capitolo 1', 'PARTE I — SPEGNERE LA SPERANZA'),
    ('2.md', 'Capitolo 2', None),
    ('3.md', 'Capitolo 3', None),
    ('SOGLIA_1.md', 'Soglia I', None),
    ('4.md', 'Capitolo 4', 'PARTE II — INSTALLARE LA PAURA'),
    ('5.md', 'Capitolo 5', None),
    ('6.md', 'Capitolo 6', None),
    ('7.md', 'Capitolo 7', None),
    ('SOGLIA_2.md', 'Soglia II', None),
    ('8.md', 'Capitolo 8', 'PARTE III — AVVELENARE I LEGAMI'),
    ('9.md', 'Capitolo 9', None),
    ('10.md', 'Capitolo 10', None),
    ('11.md', 'Capitolo 11', None),
    ('SOGLIA_3.md', 'Soglia III', None),
    ('12.md', 'Capitolo 12', 'PARTE IV — TRADIRE'),
    ('13.md', 'Capitolo 13', None),
    ('14.md', 'Capitolo 14', None),
    ('15.md', 'Capitolo 15', None),
    ('SOGLIA_4.md', 'Soglia IV', None),
    ('16.md', 'Capitolo 16', 'PARTE V — IL FONDO'),
    ('17.md', 'Capitolo 17', None),
    ('18.md', 'Capitolo 18', None),
    ('19.md', 'Capitolo 19', None),
    ('20.md', 'Capitolo 20', None),
    ('SOGLIA_5.md', 'Soglia V', None),
    ('21.md', 'Epilogo', 'EPILOGO — IL CAPITOLO SPECCHIO'),
    ('QUARTA_DI_COPERTINA.md', 'Quarta di copertina', None),
]

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    return s

def md_to_html(text):
    out=[]; paras=[]; in_ul=False; in_ol=False; bq_lines=[]
    def flush_p():
        nonlocal paras
        if paras:
            out.append('<p>' + '<br>'.join(inline(x) for x in paras) + '</p>'); paras=[]
    def flush_bq():
        nonlocal bq_lines
        if bq_lines:
            out.append('<blockquote>' + ' '.join(inline(x) for x in bq_lines) + '</blockquote>')
            bq_lines=[]
    def close_lists():
        nonlocal in_ul,in_ol
        if in_ul: out.append('</ul>'); in_ul=False
        if in_ol: out.append('</ol>'); in_ol=False
    for raw in text.splitlines():
        line=raw.rstrip()
        if not line:
            flush_p(); flush_bq(); close_lists(); continue
        if line.strip()=='---':
            flush_p(); flush_bq(); close_lists(); out.append('<hr>'); continue
        m=re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_p(); flush_bq(); close_lists()
            lvl=len(m.group(1)); out.append(f'<h{lvl}>{inline(m.group(2))}</h{lvl}>'); continue
        if line.startswith('> '):
            flush_p(); close_lists(); bq_lines.append(line[2:]); continue
        flush_bq()
        m=re.match(r'^[-*]\s+(.*)$', line)
        if m:
            flush_p()
            if not in_ul: close_lists(); out.append('<ul>'); in_ul=True
            out.append(f'<li>{inline(m.group(1))}</li>'); continue
        m=re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            flush_p()
            if not in_ol: close_lists(); out.append('<ol>'); in_ol=True
            out.append(f'<li>{inline(m.group(2))}</li>'); continue
        paras.append(line)
    flush_p(); flush_bq(); close_lists()
    return '\n'.join(out)

def section_kind(filename):
    if filename.startswith('SOGLIA'): return 'threshold'
    if filename == 'AVVERTENZA.md': return 'avvertenza'
    if filename == 'QUARTA_DI_COPERTINA.md': return 'quarta'
    return 'chapter'

items=[]
sections=[]
for filename, label, part in ORDER:
    text=(ROOT/filename).read_text(encoding='utf-8').strip()
    title=text.splitlines()[0].lstrip('# ').strip()
    anchor=Path(filename).stem.lower()
    kind=section_kind(filename)
    items.append({'href':'#'+anchor,'label':label,'title':title,'part':part,'kind':kind})
    part_html = f'<div class="part-label">{html.escape(part)}</div>' if part else ''
    sections.append(f'<section id="{anchor}" class="entry {kind}">{part_html}{md_to_html(text)}</section>')

def nav_class(kind):
    if kind == 'avvertenza': return ' class="nav-avvertenza"'
    if kind == 'quarta': return ' class="nav-quarta"'
    if kind == 'threshold': return ' class="nav-threshold"'
    return ''

nav_parts = []
prev_kind = None
for i in items:
    if prev_kind == 'avvertenza' and i['kind'] != 'avvertenza':
        nav_parts.append('<div class="nav-sep"></div>')
    if i['kind'] == 'quarta':
        nav_parts.append('<div class="nav-sep"></div>')
    nc = nav_class(i['kind'])
    nav_parts.append(f'<a href="{i["href"]}"{nc}><span>{html.escape(i["label"])}</span>{html.escape(i["title"])}</a>')
    prev_kind = i['kind']

nav = '\n'.join(nav_parts)
content='\n'.join(sections)
(DOCS/'index.html').write_text(f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Da welfare a warfare</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero">
  <p class="eyebrow">Satira manageriale in discesa controllata</p>
  <h1>Da welfare<br>a warfare</h1>
  <p class="hero-sub">Manuale di management per l&apos;estinzione del talento</p>
  <a class="skip" href="#avvertenza">Inizia a leggere</a>
</header>
<div class="layout">
  <nav aria-label="Indice"><h2>Indice</h2>{nav}</nav>
  <main>{content}</main>
</div>
<footer>Edizione web &mdash; <em>Da welfare a warfare</em> &mdash; Satira nella tradizione di Swift</footer>
</body></html>''', encoding='utf-8')
print('Wrote docs/index.html with', len(items), 'entries')
